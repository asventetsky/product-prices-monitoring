# pylint: disable=unused-argument
# pylint: disable=broad-exception-caught

""" Application logic """

import logging
import json
import s3fs
import os

from src.repository import get_products, get_product, get_product_price


logging.getLogger().setLevel(logging.INFO)

s3 = s3fs.S3FileSystem(
    anon=False,
    endpoint_url=os.environ.get('S3_ENDPOINT', f"https://s3.{os.environ['REGION']}.amazonaws.com")
)

S3_BUCKET_CACHE_NAME = os.environ['S3_BUCKET_CACHE_NAME']


def handler(event, context):
    """Contains main logic for providing historic prices for a particular product"""

    # TODO: extract service layer that handles cache and repository calls
    try:
        request = _parse_request(event)

        if request["pathParameters"]:
            handle_get_product_prices(request)
        else:
            handle_get_products()
    except Exception as error:
        logging.error("Error on providing historic prices: %s", error)
        return construct_error_response()


def handle_get_products():
    products = get_products()
    products = [{"id": product['id']['N'], "name": product['name']['S']} for product in products ]
    return construct_response(products)


def handle_get_product_prices(request):
    product_id = request["pathParameters"]["id"]
    combined_product = get_from_cache(product_id, request["period"])
    if combined_product is None:
        product = get_product(product_id)
        logging.info("Product: %s", product)

        product_prices = get_product_price(product_id, request["period"])
        logging.info("Product price: %s", product_prices)

        combined_product = combine_product_and_prices(product, product_prices)
        save_in_cache(product_id, request["period"], combined_product)

    return construct_response(combined_product)

def _parse_request(event):
    try:
        query_parameters = event["queryStringParameters"]
        return {
            "resource": event["resource"],
            "pathParameters": event["pathParameters"],
            "productId": query_parameters["productId"],
            "period": {
                "from": query_parameters["from"],
                "to": query_parameters["to"],
            },
        }
    except KeyError as error:
        logging.error(
            "Error on parsing request: %s. Original message: %s", error, event
        )

def get_from_cache(product_id, period):
    cache_path=f"{S3_BUCKET_CACHE_NAME}/{product_id}_{period['from']}-{period['to']}"
    if s3.exists(cache_path):
        logging.info("Got historic product prices from cache for product_id %s and period %s", product_id, period)
        with s3.open(cache_path, 'rb') as f:
            return json.load(f)
    else:
        logging.info("Cache MISS for product_id %s and period %s", product_id, period)

def save_in_cache(product_id, period, data):
    if data:
        cache_path=f"{S3_BUCKET_CACHE_NAME}/{product_id}_{period['from']}-{period['to']}"
        with s3.open(cache_path, 'w') as f:
            json.dump(data, f)
        logging.info("Save cache for product_id %s and period %s", product_id, period)


def combine_product_and_prices(product, product_prices):
    return {
        'product': {
            'name': product['Items'][0]['name']['S'],
            'prices': [{pp['date']['S']: pp['shownPrice']['N']} for pp in product_prices['Items']]
        }
    }

def construct_response(result):
    """Constructs final response"""

    response = {"headers": {"Content-Type": "application/json"}}

    if result:
        response["statusCode"] = 200
        response["body"] = json.dumps(result)
    else:
        response["statusCode"] = 500
        response["body"] = json.dumps({"error": "Internal server error"})

    logging.info("Response: %s", response)

    return response

def construct_error_response():
    """Constructs error response"""

    return {
        "statusCode": 500,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps({"error": "Internal server error"}),
    }
