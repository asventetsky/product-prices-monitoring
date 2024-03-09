# pylint: disable=unused-argument
# pylint: disable=broad-exception-caught

""" Application logic """

import json
import logging

from src.service import fetch_product_price
from src.service import store_product_price


logging.getLogger().setLevel(logging.INFO)


def handler(event, context):
    """Contains main logic for handling product price fetching"""

    for record in event["Records"]:
        logging.info("Record has been received: %s", record)
        request = parse_request(record)
        if request:
            product_price = fetch_product_price(request)
            if product_price:
                store_product_price(product_price)

def parse_request(record):
    try:
        body_string = record["Sns"]["Message"].replace("'", '"')
        body = json.loads(body_string)
        return {
            "url": body["url"],
            "queryParams": body["queryParams"],
            "headers": body["headers"],
            "timeoutSeconds": body["timeoutSeconds"]
        }
    except Exception as error:
        logging.error(
            "Error on parsing request: %s. Original message: %s", error, record
        )
