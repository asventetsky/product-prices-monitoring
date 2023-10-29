# pylint: disable=unused-argument
# pylint: disable=import-error

""" Application logic """

import json
import logging

from src.service import fetch_product_price

logging.getLogger().setLevel(logging.INFO)


def lambda_handler(event, context):
    """Contains main logic for handling fetching the product price"""

    price = fetch_product_price()
    return construct_response(price)


def construct_response(price):
    """Constructs final response"""

    response = {"headers": {"Content-Type": "application/json"}}

    if price:
        response["statusCode"] = 200
        response["body"] = json.dumps({"product": price})
    else:
        response["statusCode"] = 500
        response["body"] = json.dumps({"error": "Internal server error"})

    logging.info("Response: %s", response)

    return response
