resource "aws_sqs_queue" "queue" {
  name                      = var.name
#  delay_seconds             = 90
#  max_message_size          = 2048
  message_retention_seconds = 86400
#  receive_wait_time_seconds = 10
  redrive_policy = jsonencode({
    deadLetterTargetArn = aws_sqs_queue.queue_deadletter.arn
    maxReceiveCount     = 4
  })

  tags = var.resource_tags
}

resource "aws_sqs_queue" "queue_deadletter" {
  name = "${var.name}-deadletter"
}

resource "aws_sqs_queue_redrive_allow_policy" "example" {
  queue_url = aws_sqs_queue.queue_deadletter.id

  redrive_allow_policy = jsonencode({
    redrivePermission = "byQueue",
    sourceQueueArns   = [aws_sqs_queue.queue.arn]
  })
}

resource "aws_lambda_event_source_mapping" "this" {
  event_source_arn = aws_sqs_queue.queue.arn
  function_name    = var.lambda_arn
  batch_size       = 1
}
