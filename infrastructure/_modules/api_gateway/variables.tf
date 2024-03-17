variable "api_gateway_name" {}

variable "cognito_auth" {
  description = "Enable Cognito Authorization for API Gateway"
  type = bool
}

variable "stage" {}

variable "integrations" {
  description = "List of API Gateway routes with integrations"
  type        = map(object({
    lambda_invoke_arn = string
    lambda_function_name = string
  }))
  default = {}
}
