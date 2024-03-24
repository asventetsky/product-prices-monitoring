import boto3
import os
import json

client = boto3.client("dynamodb", region_name=os.environ["AWS_REGION"])
OLD_TABLE_NAME = os.environ["OLD_TABLE_NAME"]
NEW_TABLE_NAME = os.environ["NEW_TABLE_NAME"]


def fetch_product_prices():
    # print("Fetching product prices...")
    # response = client.scan(TableName=OLD_TABLE_NAME)
    # return response['Items']

    with open('product_prices.txt', 'r') as file:
        return json.load(file)


def store_product_prices(product_prices):
    print("Storing product prices...")

    with open('product_prices.txt', 'w') as file:
        json.dump(product_prices, file, indent=4)


def adjust_date_format(product_prices):
    print("Adjusting date in each product price...")
    for price in product_prices:
        price['date']['S'] = "{2}-{1}-{0}".format(*price['date']['S'].split('-'))

    return product_prices


def upload_adjusted_prices(product_prices):
    # batch_write_item accepts at most 25 put requests per each call
    # so we have to split list into smaller ones
    chunk = 25
    product_prices_chunks = [product_prices[x:x + 25] for x in range(0, len(product_prices), chunk)]

    for index, chunk in enumerate(product_prices_chunks, start=1):
        print(f"Uploading {index} chunk of adjusted product prices...")

        # Don't forget to wrap each item in 'PutRequest' & 'Item'
        upload_request = {
            NEW_TABLE_NAME: [{'PutRequest': {'Item': item}} for item in chunk]
        }

        client.batch_write_item(RequestItems=upload_request)


def main():
    product_prices = fetch_product_prices()
    # store_product_prices(product_prices)
    adjusted_product_prices = adjust_date_format(product_prices)
    upload_adjusted_prices(adjusted_product_prices)


if __name__ == "__main__":
    main()
