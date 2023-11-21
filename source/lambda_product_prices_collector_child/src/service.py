""" Service for sending request to external resource """

import logging


from datetime import date
from src.lambda_exception import LambdaException
from src.client import send_request
from src.repository import put_product
from src.repository import put_product_price

logging.getLogger().setLevel(logging.INFO)


def fetch_product_price(request):
    """Fetch and construct product price"""

    try:
        response = send_request(request)
        if response:
            product_price = _construct_product_price(response)
            logging.info(
                "Successfully fetched product price: %s", product_price
            )
            return product_price
    except LambdaException as error:
        logging.error(error.message)
        return None


def store_product_price(product_price):
    """Stores product price"""

    try:
        put_product(product_price)
        put_product_price(product_price)
    except LambdaException as error:
        logging.error(error.message)
        return None


def _construct_product_price(response):
    """Construct product price from the response"""

    try:
        response_product_price = response["data"]["storeProductInfoDTO"]
        product_price = {
            "id": int(response_product_price["id"]),
            "name": response_product_price["name"],
            "price": {
                "regularPrice": response_product_price["regularPrice"],
                "salePrice": response_product_price["salePrice"],
                "loyaltyPrice": response_product_price["loyaltyPrice"],
                "shownPrice": response_product_price["shownPrice"]
            },
            "date": date.today()
        }
        return product_price
    except Exception as exception:
        raise LambdaException(
            f"Error on extracting the product price. "
            f"Original response: `{response}`"
        ) from exception
