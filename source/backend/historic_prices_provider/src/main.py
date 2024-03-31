# pylint: disable=unused-argument
# pylint: disable=broad-exception-caught

""" Application logic """

import logging
import json

from src.repository import get_product, get_product_price


logging.getLogger().setLevel(logging.INFO)


def handler(event, context):
    """Contains main logic for providing historic prices for a particular product"""

    try:
        request = _parse_request_query_params(event)
        product = get_product(request["productId"])
        product_prices = get_product_price(request["productId"], request["period"])
        combined_product = combine_product_and_prices(product, product_prices)
        return construct_response(combined_product)
    except Exception:
        return construct_error_response()


def _parse_request_query_params(event):
    try:
        query_parameters = event["queryStringParameters"]
        return {
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

def combine_product_and_prices(product, product_prices):
    return {
        'name': product['Items'][0]['name']['S'],
        'prices': [{pp['date']['S']: pp['shownPrice']['N']} for pp in product_prices['Items']]
    }

def construct_response(combined_product):
    """Constructs final response"""

    response = {"headers": {"Content-Type": "application/json"}}

    if combined_product:
        response["statusCode"] = 200
        response["body"] = json.dumps({"product": combined_product})
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
