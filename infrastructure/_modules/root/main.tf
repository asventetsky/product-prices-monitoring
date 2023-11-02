#================================================#
# PRICES COLLECTOR: lambda function and iam role #
#================================================#
data "aws_iam_policy_document" "prices_collector" {
  statement {
    actions   = ["logs:CreateLogStream", "logs:PutLogEvents"]
    resources = ["arn:aws:logs:*:*:*"]
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
    PRODUCTS_URL = var.products_url
    PRODUCTS_TIMEOUT = var.products_timeout
  }

  resource_tags = var.resource_tags
}
