variable "region" {}

variable "env" {}

variable "app_name" {}

variable "lambda_prices_collector_image_uri" {}

variable "lambda_prices_collector_schedule" {}

variable "products_url" {}

variable "products_timeout" {}

variable "resource_tags" {
  type = map(string)
}
