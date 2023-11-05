# pylint: disable=unused-argument
# pylint: disable=import-error

""" Application logic """

import logging
import os
import boto3
import json

logging.getLogger().setLevel(logging.INFO)

client = boto3.client('sqs')


def handler(event, context):
    """Contains main logic for creating tasks for fetching product prices"""

    products_json_string = os.environ["PRODUCTS_JSON_STRING"]
    products = json.loads(products_json_string)

    logging.info(f"Prepared {len(products)} product(s) for fetching prices: {products}")

    for product in products:
        client.send_message(
            QueueUrl=os.environ["PRODUCTS_QUEUE_URL"],
            MessageBody=str(product)
        )

    logging.info(f"Successfully created tasks for processing")
