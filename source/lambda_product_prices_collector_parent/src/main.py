# pylint: disable=unused-argument

""" Application logic """

import logging
import os
import boto3
import json

logging.getLogger().setLevel(logging.INFO)

client = boto3.client("sns")


def handler(event, context):
    """Contains main logic for creating tasks for fetching product prices"""

    products_json_string = os.environ["PRODUCTS_JSON_STRING"]
    products = json.loads(products_json_string)

    logging.info(
        "Prepared %s product(s) for fetching prices: %s",
        len(products["items"]),
        products
    )

    url = products["url"]
    query_params = products["queryParams"]
    timeout_seconds = products["timeoutSeconds"]

    for product in products["items"]:
        # TODO: wrap with try-except in order to catch errors
        # TODO: remove `path` field from message
        product["url"] = url + product["path"]
        product["queryParams"] = query_params
        product["timeoutSeconds"] = timeout_seconds
        client.publish(
            TopicArn=os.environ["PRODUCTS_TOPIC_ARN"],
            Message=str(product)
        )

    # TODO: log number of created tasks
    logging.info("Successfully created tasks for processing")
