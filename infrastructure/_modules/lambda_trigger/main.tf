resource "aws_cloudwatch_event_rule" "trigger" {
  name = "${var.lambda_name}_trigger"
  schedule_expression = var.schedule
}

resource "aws_cloudwatch_event_target" "trigger" {
  rule = aws_cloudwatch_event_rule.trigger.name
  target_id = "${var.lambda_name}_trigger"
  arn = var.lambda_arn
}


resource "aws_lambda_permission" "trigger" {
  action = "lambda:InvokeFunction"
  function_name = var.lambda_name
  principal = "events.amazonaws.com"
  source_arn = aws_cloudwatch_event_rule.trigger.arn
}
