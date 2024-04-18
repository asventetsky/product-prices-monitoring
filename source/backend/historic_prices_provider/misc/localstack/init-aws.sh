#!/bin/bash

awslocal dynamodb create-table \
  --table-name product-prices \
  --attribute-definitions AttributeName=product_id,AttributeType=N AttributeName=date,AttributeType=S \
  --key-schema AttributeName=product_id,KeyType=HASH AttributeName=date,KeyType=RANGE \
  --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5 \
  --region eu-central-1

awslocal dynamodb create-table \
  --table-name products \
  --attribute-definitions AttributeName=id,AttributeType=N \
  --key-schema AttributeName=id,KeyType=HASH \
  --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5 \
  --region eu-central-1

awslocal dynamodb batch-write-item \
  --request-items file://products-items.json \
  --region eu-central-1

awslocal dynamodb batch-write-item \
  --request-items file://product-prices-items.json \
  --region eu-central-1

awslocal s3api create-bucket \
  --bucket historic-prices-provider-cache-bucket \
  --create-bucket-configuration LocationConstraint=eu-central-1