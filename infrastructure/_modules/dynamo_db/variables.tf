variable "table_name" {}

variable "partition_key" {}

variable "range_key" {
  default = null
}

variable "resource_tags" {
  type = map(string)
}
