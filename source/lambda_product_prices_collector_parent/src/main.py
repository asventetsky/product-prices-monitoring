# pylint: disable=unused-argument
# pylint: disable=import-error

""" Application logic """

import logging
import os
import boto3
import json

logging.getLogger().setLevel(logging.INFO)

client = boto3.client('sns')


def handler(event, context):
    """Contains main logic for creating tasks for fetching product prices"""

    products_json_string = os.environ["PRODUCTS_JSON_STRING"]
    products = json.loads(products_json_string)

    logging.info(f"Prepared {len(products)} product(s) for fetching prices: {products}")

    for product in products:
        # TODO: wrap with try-except in order to catch errors
        client.publish(
            TopicArn=os.environ["PRODUCTS_TOPIC_ARN"],
            Message=str(product)
        )

    # TODO: log number of created tasks
    logging.info(f"Successfully created tasks for processing")
