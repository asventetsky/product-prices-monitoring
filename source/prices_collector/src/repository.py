""" Access to the database """

import logging
import os

import botocore
import boto3

client = boto3.client("dynamodb", region_name=os.environ["REGION"])
PRODUCTS_TABLE_NAME = os.environ["PRODUCTS_TABLE_NAME"]
PRODUCT_PRICES_TABLE_NAME = os.environ["PRODUCT_PRICES_TABLE_NAME"]

logging.getLogger().setLevel(logging.INFO)


def put_record(product_price):
    """Puts record into DynamoDb"""

    try:
        client.put_item(
            TableName=PRODUCTS_TABLE_NAME,
            Item={
                "id": {"N": str(product_price["id"])},
                "name": {"S": product_price["name"]}
            }
        )
    except botocore.exceptions.ClientError as error:
        logging.error(f"Error occurred while saving product: {error}")

    try:
        client.put_item(
            TableName=PRODUCT_PRICES_TABLE_NAME,
            Item={
                "product_id": {"N": str(product_price["id"])},
                "regularPrice": {"N": str(product_price["regularPrice"])},
                "salePrice": {"N": str(product_price["salePrice"])},
                "loyaltyPrice": {"N": str(product_price["loyaltyPrice"])},
                "shownPrice": {"N": str(product_price["shownPrice"])},
                "date": {"S": product_price["date"].strftime("%d-%m-%Y")}
            }
        )
    except botocore.exceptions.ClientError as error:
        logging.error(f"Error occurred while saving product price: {error}")
