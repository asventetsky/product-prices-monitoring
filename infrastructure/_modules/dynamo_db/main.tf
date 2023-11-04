resource "aws_dynamodb_table" "this" {
  name = var.table_name
  billing_mode = "PROVISIONED"
  read_capacity= "5"
  write_capacity= "5"

  attribute {
    name = var.partition_key
    type = "N"
  }

  hash_key = var.partition_key

  tags = var.resource_tags
}
