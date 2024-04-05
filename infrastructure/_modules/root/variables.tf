variable "region" {}

variable "env" {}

variable "app_name" {}

variable "lambda_product_prices_collector_schedule" {}

variable "lambda_product_prices_collector_parent_image_uri" {}

variable "lambda_product_prices_collector_child_image_uri" {}

variable "lambda_historic_prices_provider_image_uri" {}

variable "resource_tags" {
  type = map(string)
}
