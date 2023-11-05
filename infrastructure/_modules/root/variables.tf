variable "region" {}

variable "env" {}

variable "app_name" {}

variable "products_json_string" {}

variable "lambda_product_prices_collector_schedule" {}

variable "lambda_product_prices_collector_parent_image_uri" {}

variable "lambda_product_prices_collector_child_image_uri" {}

variable "products_url" {}

variable "products_url_provide_timestamp" {}

variable "products_timeout" {}

variable "resource_tags" {
  type = map(string)
}
