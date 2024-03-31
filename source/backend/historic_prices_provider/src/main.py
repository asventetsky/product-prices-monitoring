# pylint: disable=unused-argument
# pylint: disable=broad-exception-caught

""" Application logic """

import logging
import json

from src.repository import get_product, get_product_price


logging.getLogger().setLevel(logging.INFO)


def handler(event, context):
    """Contains main logic for providing historic prices for a particular product"""

    request = _parse_request_query_params(event)
    product = get_product(request["productId"])
    # logging.info(
    #     "Product: %s", product
    # )
    # Product: {'Items': [{'name': {'S': 'Akmina +C Vitaminli Limon Aromalı Maden Suyu 6X200 Ml'}, 'id': {'N': '20000008040938'}}], 'Count': 1, 'ScannedCount': 1, 'ResponseMetadata': {'RequestId': '4b8ec03e-4f07-476b-ae74-51e0a61d8c7a', 'HTTPStatusCode': 200, 'HTTPHeaders': {'content-type': 'application/x-amz-json-1.0', 'content-length': '152', 'x-amzn-requestid': '4b8ec03e-4f07-476b-ae74-51e0a61d8c7a', 'x-amz-crc32': '522622298', 'connection': 'close', 'date': 'Sun, 31 Mar 2024 13:47:46 GMT', 'server': 'hypercorn-h11'}, 'RetryAttempts': 0}}

    product_prices = get_product_price(request["productId"], request["period"])
    # logging.info(
    #     "Product price: %s", product_price
    # )
    # Product price: {'Items': [{'date': {'S': '2024-03-26'}, 'shownPrice': {'N': '13000'}, 'product_id': {'N': '20000008040938'}}, {'date': {'S': '2024-03-27'}, 'shownPrice': {'N': '13100'}, 'product_id': {'N': '20000008040938'}}, {'date': {'S': '2024-03-28'}, 'shownPrice': {'N': '13200'}, 'product_id': {'N': '20000008040938'}}], 'Count': 3, 'ScannedCount': 3, 'ResponseMetadata': {'RequestId': 'c618bce3-8a7a-4492-b1f6-e719aef85f62', 'HTTPStatusCode': 200, 'HTTPHeaders': {'content-type': 'application/x-amz-json-1.0', 'content-length': '342', 'x-amzn-requestid': 'c618bce3-8a7a-4492-b1f6-e719aef85f62', 'x-amz-crc32': '611840207', 'connection': 'close', 'date': 'Sun, 31 Mar 2024 13:47:46 GMT', 'server': 'hypercorn-h11'}, 'RetryAttempts': 0}}

    combined_product = combine_product_and_prices(product, product_prices)

    return construct_response(combined_product)


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
    combined_product = {}
    combined_product['name'] = product['Items'][0]['name']['S']
    combined_product['prices'] = [{product_price['date']['S']: product_price['shownPrice']['N']} for product_price in product_prices['Items']]
    logging.info(
        "Combined: %s", combined_product
    )
    return combined_product

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
