# pylint: disable=unused-argument
# pylint: disable=broad-exception-caught

""" Application logic """

import logging

from repository import get_product_price


logging.getLogger().setLevel(logging.INFO)


def handler(event, context):
    """Contains main logic for providing historic prices for a particular product"""

    request = _parse_request_query_params(event)
    product_price = get_product_price(request["productId"], request["period"])
    logging.info(
        "Product price: %s", product_price
    )


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

if __name__ == "__main__":
    event = {
        "queryStringParameters": {
            "productId": "20000010350036",
            "from": "2023-12-01",
            "to": "2023-12-12",

        }
    }
    handler(event, {})
