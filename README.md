# Product prices monitoring app
> Solution for tracking and visualising prices of the shop.

## Developing

### Run unit tests
Within the source code of lambda (eg. `source/lambda_product_prices_collector_parent` or
`source/lambda_product_prices_collector_child`) execute the following command:
```shell
python3 -m unittest discover test
```

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

## Set up Cognito user

### Fetch user_pool_id
```bash
aws cognito-idp list-user-pools \
  --max-results 1 \
  --query "UserPools[?starts_with(Name, 'combination-api-app')].Id | [0]"
```

### Fetch user_pool_client_id
```bash
aws cognito-idp list-user-pool-clients \
  --user-pool-id [user_pool_id] \
  --query "UserPoolClients[?starts_with(ClientName, 'combination-api-app')].ClientId | [0]"
```

### Create Cognito user
```bash
aws cognito-idp sign-up \
  --client-id [user_pool_client_id] \
  --username [username] \
  --password [password] \
  --user-attributes Name=email,Value=[email]
```

### Confirm Cognito user
If `"confirm_email_option": "CONFIRM_WITH_LINK"` a user can be confirmed by a link in the email that has been provided
during the registration.
Otherwise, if `"confirm_email_option": "CONFIRM_WITH_LINK"`, the user receives email with verification code. Next, the user
should be confirmed by executing the following command:
```bash
aws cognito-idp confirm-sign-up \
  --client-id [user_pool_client_id] \
  --username=[username] \
  --confirmation-code [verification_code_from_email]
```

### Get token
```bash
aws cognito-idp initiate-auth \
  --client-id [user_pool_client_id] \
  --auth-flow USER_PASSWORD_AUTH \
  --auth-parameters USERNAME=[username],PASSWORD=[password] \
  --query 'AuthenticationResult.IdToken' \
  --output text
```
