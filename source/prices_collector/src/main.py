# pylint: disable=unused-argument
# pylint: disable=import-error

""" Application logic """

import logging

from src.service import fetch_product_price
from src.repository import put_record

logging.getLogger().setLevel(logging.INFO)


def handler(event, context):
    """Contains main logic for handling fetching the product price"""

    product_price = fetch_product_price()
    put_record(product_price)
