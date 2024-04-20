variable "api_gateway_name" {}

variable "cognito_auth" {
  description = "Enable Cognito Authorization for API Gateway"
  type = bool
}

variable "stage" {}

variable "lambda_invoke_arn" {}

variable "lambda_function_name" {}
