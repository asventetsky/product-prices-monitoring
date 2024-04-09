""" Access to the database """

import logging
import os

import botocore
import boto3

client = boto3.client(
    "dynamodb",
    region_name=os.environ["REGION"],
    endpoint_url=os.environ.get('DYNAMODB_ENDPOINT', f"https://dynamodb.{os.environ['REGION']}.amazonaws.com")
)
PRODUCTS_TABLE_NAME = os.environ["PRODUCTS_TABLE_NAME"]
PRODUCT_PRICES_TABLE_NAME = os.environ["PRODUCT_PRICES_TABLE_NAME"]

logging.getLogger().setLevel(logging.INFO)

def get_product(product_id):
    logging.info(
        "product_id: %s", product_id
    )

    try:
        return client.query(
            TableName=PRODUCTS_TABLE_NAME,
            ProjectionExpression="id, #nm",
            ExpressionAttributeNames={"#nm": "name"},
            KeyConditionExpression="id = :v1",
            ExpressionAttributeValues={
                ":v1": {"N": product_id}
            },
        )
    except botocore.exceptions.ClientError as error:
        logging.error("Unable to get product by id `%s`: %s", product_id, error)


def get_product_price(product_id, period):
    logging.info(
        "product_id: %s, period: %s", product_id, period
    )

    try:
        return client.query(
            TableName=PRODUCT_PRICES_TABLE_NAME,
            ProjectionExpression="product_id, #dt, shownPrice",
            ExpressionAttributeNames={"#dt": "date"},
            KeyConditionExpression="product_id = :v1 AND #dt BETWEEN :v2a AND :v2b",
            ExpressionAttributeValues={
                ":v1": {"N": product_id},
                ":v2a": {"S": period["from"]},
                ":v2b": {"S": period["to"]}
            },
        )
    except botocore.exceptions.ClientError as error:
        logging.error("Unable to get product price by product_id `%s`: %s", product_id, error)
