variable "region" {}

variable "env" {}

variable "name" {}

variable "image_uri" {}

variable "lambda_role_arn" {}

variable "environment_variables" {
  type = map(string)
}

variable "resource_tags" {
  type = map(string)
}
