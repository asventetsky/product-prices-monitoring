# Product prices monitoring app
> Solution for tracking and visualising prices of the shop.

## Developing

### Building and pushing docker image to Amazon ECR
Within the source code of lambda (eg. `source/lambda_product_prices_collector_parent` or
`source/lambda_product_prices_collector_child`) execute the following script:
```shell
../../misc/build_push_lambda_image.sh <aws_account_id> <aws_region>
```

### Test the image locally
< TODO: run with `docker compose` (2 lambdas + SNS + DynamoDB) >

### Terragrunt apply
Initialize Terragrunt:
```shell
terragrunt init
```
Apply the configuration:
```shell
terragrunt apply
```
Remove all the created artifacts:
```shell
terragrunt destroy
```

### Run the lambda
```shell
aws lambda invoke --function-name lambda_prices_collector-<aws_region>-<environment> response.json
```
