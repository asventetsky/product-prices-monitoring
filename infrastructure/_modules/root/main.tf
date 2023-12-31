#=========================================================#
# SNS for tasks exchange between parent and child lambdas #
#=========================================================#
module "sns_product_prices" {
  source = "../../../../../_modules/sns"

  name = "product-prices-${var.region}-${var.env}-topic"
  lambda_name = module.lambda_product_prices_collector_child.lambda_name
  lambda_arn = module.lambda_product_prices_collector_child.lambda_arn

  resource_tags = var.resource_tags
}

#=====================================#
# DynamoDB for storing product prices #
#=====================================#
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
  range_key = "date"

  resource_tags = var.resource_tags
}

#========================================================================#
# PRODUCT PRICES COLLECTOR PARENT: lambda function, iam role and trigger #
#========================================================================#
data "aws_iam_policy_document" "lambda_product_prices_collector_parent" {
  statement {
    actions   = ["logs:CreateLogStream", "logs:PutLogEvents"]
    resources = ["arn:aws:logs:*:*:*"]
    effect = "Allow"
  }
  statement {
    actions   = ["sns:Publish"]
    resources = [module.sns_product_prices.arn]
    effect = "Allow"
  }
}

module "lambda_product_prices_collector_parent_iam_role" {
  source = "github.com/asventetsky/freecodecamp-aws-serverless-projects-common//terraform/module/aws/lambda_iam_role?ref=1c71f0bcea456cecbedfc8b67cc540144217bb8d"

  region = var.region
  env = var.env
  lambda_name = "lambda_product_prices_collector_parent"
  policy_json_string = data.aws_iam_policy_document.lambda_product_prices_collector_parent.json

  resource_tags = var.resource_tags
}

module "lambda_product_prices_collector_parent" {
  source = "../../../../../_modules/lambda_docker_image"

  name = "lambda_product_prices_collector_parent"
  region = var.region
  env = var.env
  lambda_role_arn = module.lambda_product_prices_collector_parent_iam_role.arn
  image_uri = var.lambda_product_prices_collector_parent_image_uri

  environment_variables = {
    PRODUCTS_JSON_STRING = data.aws_ssm_parameter.products_json_string.value
    PRODUCTS_TOPIC_ARN = module.sns_product_prices.arn
  }

  resource_tags = var.resource_tags
}

module "lambda_product_prices_collector_parent_trigger" {
  source = "../../../../../_modules/lambda_trigger"

  schedule = var.lambda_product_prices_collector_schedule
  lambda_arn = module.lambda_product_prices_collector_parent.lambda_arn
  lambda_name = module.lambda_product_prices_collector_parent.lambda_name

}

data "aws_ssm_parameter" "products_json_string" {
  name = "/${var.env}/products_json_string"
}

#==============================================================#
# PRODUCT PRICES COLLECTOR CHILD: lambda function and iam role #
#==============================================================#
data "aws_iam_policy_document" "product_prices_collector_child" {
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
  lambda_name = "lambda_product_prices_collector_child"
  policy_json_string = data.aws_iam_policy_document.product_prices_collector_child.json

  resource_tags = var.resource_tags
}

module "lambda_product_prices_collector_child" {
  source = "../../../../../_modules/lambda_docker_image"

  name = "lambda_product_prices_collector_child"
  region = var.region
  env = var.env
  lambda_role_arn = module.lambda_prices_collector_iam_role.arn
  image_uri = var.lambda_product_prices_collector_child_image_uri

  environment_variables = {
    REGION = var.region
    PRODUCTS_TABLE_NAME = module.dynamo_db_products_table.table_name
    PRODUCT_PRICES_TABLE_NAME = module.dynamo_db_product_prices_table.table_name
  }

  resource_tags = var.resource_tags
}
