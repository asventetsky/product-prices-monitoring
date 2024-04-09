# Lambda: historic prices provider
> Provides prices for a specified period (`from` - `to`).

## Developing

### Running locally

```shell
cd backend/historic_prices_provider/misc
```

```shell
docker compose up
```

```shell
aws dynamodb create-table \
--table-name product-prices \
--attribute-definitions AttributeName=product_id,AttributeType=N AttributeName=date,AttributeType=S \
--key-schema AttributeName=product_id,KeyType=HASH AttributeName=date,KeyType=RANGE \
--provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5 \
--endpoint-url http://localhost:4566 \
--region eu-central-1 && \
aws dynamodb create-table \
--table-name products \
--attribute-definitions AttributeName=id,AttributeType=N \
--key-schema AttributeName=id,KeyType=HASH \
--provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5 \
--endpoint-url http://localhost:4566 \
--region eu-central-1 && \
aws dynamodb batch-write-item \
--request-items file://products-items.json \
--endpoint-url http://localhost:4566 \
--region eu-central-1 && \
aws dynamodb batch-write-item \
--request-items file://product-prices-items.json \
--endpoint-url http://localhost:4566 \
--region eu-central-1 && \
aws s3api create-bucket \
    --bucket cache-bucket-example \
    --endpoint-url http://localhost:4566 \
    --create-bucket-configuration LocationConstraint=eu-central-1
```

```shell
httpie :9000/2015-03-31/functions/function/invocations queryStringParameters[productId]=20000008040938 queryStringParameters[from]=2024-03-26 queryStringParameters[to]=2024-03-28
```