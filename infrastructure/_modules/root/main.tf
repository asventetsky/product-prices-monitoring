module "dynamo_db_products_table" {
  source = "../../../../../_modules/dynamo_db"

  table_name = "products"
  partition_key = "id"

  resource_tags = var.resource_tags
}

module "dynamo_db_product_prices_table" {
  source = "../../../../../_modules/dynamo_db"

  table_name = "product_prices"
  partition_key = "product_id"

  resource_tags = var.resource_tags
}

#================================================#
# PRICES COLLECTOR: lambda function and iam role #
#================================================#
data "aws_iam_policy_document" "prices_collector" {
  statement {
    actions   = ["logs:CreateLogStream", "logs:PutLogEvents"]
    resources = ["arn:aws:logs:*:*:*"]
    effect = "Allow"
  }
  statement {
    actions   = ["dynamodb:PutItem"]
    resources = [module.dynamo_db_products_table.table_arn, module.dynamo_db_product_prices_table.table_arn]
    effect = "Allow"
  }
}

module "lambda_prices_collector_iam_role" {
  source = "github.com/asventetsky/freecodecamp-aws-serverless-projects-common//terraform/module/aws/lambda_iam_role?ref=1c71f0bcea456cecbedfc8b67cc540144217bb8d"

  region = var.region
  env = var.env
  lambda_name = "prices_collector"
  policy_json_string = data.aws_iam_policy_document.prices_collector.json

  resource_tags = var.resource_tags
}

module "lambda_prices_collector" {
  source = "../../../../../_modules/lambda_docker_image"

  name = "lambda_prices_collector"
  region = var.region
  env = var.env
  lambda_role_arn = module.lambda_prices_collector_iam_role.arn
  image_uri = var.lambda_prices_collector_image_uri

  environment_variables = {
    REGION = var.region
    PRODUCTS_URL = var.products_url
    PRODUCTS_TIMEOUT = var.products_timeout
    PRODUCTS_TABLE_NAME = module.dynamo_db_products_table.table_name
    PRODUCT_PRICES_TABLE_NAME = module.dynamo_db_product_prices_table.table_name
  }

  resource_tags = var.resource_tags
}

module "lambda_prices_collector_trigger" {
  source = "../../../../../_modules/lambda_trigger"

  schedule = var.lambda_prices_collector_schedule
  lambda_arn = module.lambda_prices_collector.lambda_arn
  lambda_name = module.lambda_prices_collector.lambda_name

}
