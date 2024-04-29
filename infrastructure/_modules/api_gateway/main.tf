resource "aws_api_gateway_rest_api" "this" {
  name = var.api_gateway_name
}

#=======================#
# Cognito configuration #
#=======================#
resource "aws_cognito_user_pool" "this" {
  count = var.cognito_auth ? 1 : 0

  name = "${aws_api_gateway_rest_api.this.name}-user-pool"

  alias_attributes           = ["email"]
  auto_verified_attributes   = ["email"]

  password_policy {
    minimum_length = 8
  }

  schema {
    attribute_data_type = "String"
    developer_only_attribute = false
    mutable = true
    name = "email"
    required = true

    string_attribute_constraints {
      min_length = 1
      max_length = 256
    }
  }

  verification_message_template {
    default_email_option = "CONFIRM_WITH_LINK" # CONFIRM_WITH_CODE
    email_subject_by_link = "Email Address Verification Request for ${var.api_gateway_name}"
    email_message_by_link = "We have received a request to authorize this email address for use with ${var.api_gateway_name}. If you requested this verification, please go to the following URL to confirm that you are authorized to use this email address:\n{##Click Here##}"
  }
}

resource "aws_cognito_user_pool_client" "this" {
  count = var.cognito_auth ? 1 : 0

  name = "${aws_api_gateway_rest_api.this.name}-user-pool-client"

  explicit_auth_flows = [
    "ALLOW_USER_PASSWORD_AUTH",
    "ALLOW_REFRESH_TOKEN_AUTH"
  ]
  user_pool_id = aws_cognito_user_pool.this[0].id
}

resource "aws_api_gateway_authorizer" "this" {
  count = var.cognito_auth ? 1 : 0

  name          = "${aws_api_gateway_rest_api.this.name}-user-pool-authorizer"
  type          = "COGNITO_USER_POOLS"
  rest_api_id   = aws_api_gateway_rest_api.this.id
  provider_arns = [aws_cognito_user_pool.this[0].arn]
}

resource "aws_cognito_user_pool_domain" "main" {
  count = var.cognito_auth ? 1 : 0

  domain       = "${aws_api_gateway_rest_api.this.name}-user-pool-domain"
  user_pool_id = aws_cognito_user_pool.this[0].id
}

resource "aws_api_gateway_deployment" "this" {
  depends_on = [aws_api_gateway_integration.root, aws_api_gateway_integration.child]

  rest_api_id = aws_api_gateway_rest_api.this.id

  triggers = {
    # NOTE: The configuration below will satisfy ordering considerations,
    #       but not pick up all future REST API changes. More advanced patterns
    #       are possible, such as using the filesha1() function against the
    #       Terraform configuration file(s) or removing the .id references to
    #       calculate a hash against whole resources. Be aware that using whole
    #       resources will show a difference after the initial implementation.
    #       It will stabilize to only change when resources change afterwards.
#    redeployment = sha1(jsonencode([
#      aws_api_gateway_resource.root.id,
#      aws_api_gateway_method.root.id,
#      aws_api_gateway_integration.root.id,
#
#      aws_api_gateway_resource.child.id,
#      aws_api_gateway_method.child.id,
#      aws_api_gateway_integration.child.id,
#
#      aws_api_gateway_resource.cors.id,
#      aws_api_gateway_method.cors.id,
#      aws_api_gateway_integration.cors.id,
#    ]))
    redeployment = filesha1("main.tf")
  }

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_api_gateway_stage" "this" {
  stage_name = var.stage
  rest_api_id = aws_api_gateway_rest_api.this.id
  deployment_id = aws_api_gateway_deployment.this.id
}

#=============================================#
# Declare resources, methods and integrations #
#=============================================#
resource "aws_api_gateway_resource" "root" {
  path_part = "products"
  parent_id = aws_api_gateway_rest_api.this.root_resource_id
  rest_api_id = aws_api_gateway_rest_api.this.id
}

resource "aws_api_gateway_resource" "child" {
  path_part = "{id}"
  parent_id = aws_api_gateway_resource.root.id
  rest_api_id = aws_api_gateway_rest_api.this.id
}

resource "aws_api_gateway_method" "root" {
  rest_api_id = aws_api_gateway_rest_api.this.id
  resource_id = aws_api_gateway_resource.root.id
  http_method = "GET"

  authorization = var.cognito_auth ? "COGNITO_USER_POOLS" : "NONE"
  authorizer_id = var.cognito_auth ? aws_api_gateway_authorizer.this[0].id : null
}

resource "aws_api_gateway_method" "child" {
  rest_api_id = aws_api_gateway_rest_api.this.id
  resource_id = aws_api_gateway_resource.child.id
  http_method = "GET"

  authorization = var.cognito_auth ? "COGNITO_USER_POOLS" : "NONE"
  authorizer_id = var.cognito_auth ? aws_api_gateway_authorizer.this[0].id : null

  request_parameters = {
    "method.request.path.id" = true
  }
}

resource "aws_lambda_permission" "this" {
  action        = "lambda:InvokeFunction"
  function_name = var.lambda_function_name
  principal     = "apigateway.amazonaws.com"

  source_arn = "${aws_api_gateway_rest_api.this.execution_arn}/*/*"
}

resource "aws_api_gateway_integration" "root" {
  rest_api_id = aws_api_gateway_rest_api.this.id
  resource_id = aws_api_gateway_resource.root.id
  http_method = aws_api_gateway_method.root.http_method

  integration_http_method = "POST"
  type = "AWS_PROXY"
  uri = var.lambda_invoke_arn
}

resource "aws_api_gateway_integration" "child" {
  rest_api_id = aws_api_gateway_rest_api.this.id
  resource_id = aws_api_gateway_resource.child.id
  http_method = aws_api_gateway_method.child.http_method

  integration_http_method = "POST"
  type = "AWS_PROXY"
  uri = var.lambda_invoke_arn

  request_parameters = {
    "integration.request.path.id" = "method.request.path.id"
  }
}

// =====
// CORS
// =====
resource "aws_api_gateway_resource" "cors" {
  rest_api_id = aws_api_gateway_rest_api.this.id
  parent_id   = aws_api_gateway_rest_api.this.root_resource_id
  path_part   = "{cors+}"
}

resource "aws_api_gateway_method" "cors" {
  rest_api_id   = aws_api_gateway_rest_api.this.id
  resource_id   = aws_api_gateway_resource.cors.id
  http_method   = "OPTIONS"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "cors" {
  rest_api_id = aws_api_gateway_rest_api.this.id
  resource_id = aws_api_gateway_resource.cors.id
  http_method = aws_api_gateway_method.cors.http_method
  type = "MOCK"
  request_templates = {
    "application/json" = jsonencode(
      {
        statusCode = 200
      }
    )
  }
}

resource "aws_api_gateway_method_response" "cors" {
  depends_on = [aws_api_gateway_method.cors]
  rest_api_id = aws_api_gateway_rest_api.this.id
  resource_id = aws_api_gateway_resource.cors.id
  http_method = aws_api_gateway_method.cors.http_method
  status_code = 200
  response_parameters = {
    "method.response.header.Access-Control-Allow-Origin" = true,
    "method.response.header.Access-Control-Allow-Methods" = true,
    "method.response.header.Access-Control-Allow-Headers" = true
  }
  response_models = {
    "application/json" = "Empty"
  }
}

resource "aws_api_gateway_integration_response" "cors" {
  depends_on = [aws_api_gateway_integration.cors, aws_api_gateway_method_response.cors]
  rest_api_id = aws_api_gateway_rest_api.this.id
  resource_id = aws_api_gateway_resource.cors.id
  http_method = aws_api_gateway_method.cors.http_method
  status_code = 200
  response_parameters = {
    "method.response.header.Access-Control-Allow-Origin" = "'*'", # replace with hostname of frontend (CloudFront)
    "method.response.header.Access-Control-Allow-Headers" = "'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'",
    "method.response.header.Access-Control-Allow-Methods" = "'GET, OPTIONS'" # remove or add HTTP methods as needed
  }
}
