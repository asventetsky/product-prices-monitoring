""" Access to the database """

import logging
import os

import botocore
import boto3

client = boto3.client("dynamodb", region_name=os.environ["REGION"])
PRODUCTS_TABLE_NAME = os.environ["PRODUCTS_TABLE_NAME"]
PRODUCT_PRICES_TABLE_NAME = os.environ["PRODUCT_PRICES_TABLE_NAME"]

logging.getLogger().setLevel(logging.INFO)


def put_product(product_price):
    """Puts product into DynamoDb"""

    try:
        item = {
            "id": {"N": str(product_price["id"])},
            "name": {"S": product_price["name"]}
        }
        client.put_item(
            TableName=PRODUCTS_TABLE_NAME,
            Item=item
        )
        logging.info(f"Successfully stored product: {item}")
    except botocore.exceptions.ClientError as error:
        logging.error(f"Error occurred while saving product: {error}")


def put_product_price(product_price):
    """Puts product price into DynamoDb"""

    try:
        item = {
            "product_id": {"N": str(product_price["id"])},
            "regularPrice": {"N": str(product_price["price"]["regularPrice"])},
            "salePrice": {"N": str(product_price["price"]["salePrice"])},
            "loyaltyPrice": {"N": str(product_price["price"]["loyaltyPrice"])},
            "shownPrice": {"N": str(product_price["price"]["shownPrice"])},
            "date": {"S": product_price["date"].strftime("%d-%m-%Y")}
        }
        client.put_item(
            TableName=PRODUCT_PRICES_TABLE_NAME,
            Item=item
        )
        logging.info(f"Successfully stored product price: {item}")
    except botocore.exceptions.ClientError as error:
        logging.error(f"Error occurred while saving product price: {error}")
