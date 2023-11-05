# pylint: disable=unused-argument
# pylint: disable=import-error

""" Application logic """

import json
import logging

from src.service import fetch_product_price
from src.service import store_product_price


logging.getLogger().setLevel(logging.INFO)


def handler(event, context):
    """Contains main logic for handling product price fetching"""

    request = parse_request(event)
    product_price = fetch_product_price(request["path"], request["referer"])
    if product_price:
        store_product_price(product_price)

def parse_request(event):
    try:
        body_string = event["Records"][0]["body"].replace("'", '"')
        body = json.loads(body_string)
        return {
            "path": body["path"],
            "referer": body["referer"]
        }
    except Exception as error:
        logging.error(f"Error on parsing request: {error}. Original message: {event}")
