resource "aws_sns_topic" "this" {
  name = var.name
}

resource "aws_sns_topic_subscription" "this" {
  topic_arn = aws_sns_topic.this.arn
  protocol  = "lambda"
  endpoint  = var.lambda_arn
}

resource "aws_lambda_permission" "this" {
  action = "lambda:InvokeFunction"
  function_name = var.lambda_name
  principal = "sns.amazonaws.com"
  source_arn = aws_sns_topic.this.arn
}