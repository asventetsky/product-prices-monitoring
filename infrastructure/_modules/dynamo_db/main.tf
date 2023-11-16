resource "aws_dynamodb_table" "this" {
  name = var.table_name
  billing_mode = "PROVISIONED"
  read_capacity= "5"
  write_capacity= "5"

  attribute {
    name = var.partition_key
    type = "N"
  }

  dynamic "attribute" {
    for_each = var.range_key != null ? [1] : []
    content {
      name = var.range_key
      type = "S"
    }
  }

  hash_key = var.partition_key
  range_key = var.range_key != null ? var.range_key : null

  tags = var.resource_tags
}
