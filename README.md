# Product prices monitoring app
> < TBD >

## Developing

### Building

Create docker image of the prices collector lambda:
```shell
docker build --platform linux/amd64 -t lambda_prices_collector:<image_tag> .
```

### Test the image locally
Run the created image with required environment variables:
```shell
docker run --env PRODUCTS_URL=<url> --env PRODUCTS_TIMEOUT=10 -p 9000:8080 lambda_prices_collector:<image_tag>
```

Invoke the lambda:
```shell
curl "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{}'
```


### Push the image to ECR
```shell
docker tag lambda_prices_collector:<image_tag> <aws_account_id>.dkr.ecr.<aws_region>.amazonaws.com/lambda_prices_collector:<image_tag>
```
```shell
aws ecr get-login-password --region <aws_region> | sudo docker login --username AWS --password-stdin <aws_account_id>.dkr.ecr.<aws_region>.amazonaws.com/lambda_prices_collector
```
```shell
sudo docker push <aws_account_id>.dkr.ecr.<aws_region>.amazonaws.com/lambda_prices_collector:<image_tag>
```

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
