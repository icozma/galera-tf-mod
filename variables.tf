# Variable declaration for database module
variable "db_node_count" {
  type    = "string"
  default = "3"
}

variable "db_node_size" {
  type    = "string"
  default = ""
}

variable "lb_size" {
  type    = "string"
  default = "c-2"
}

variable "project" {}

variable "region" {}

variable "image_slug" {
  type    = "string"
  default = "debian-9-x64"
}

variable "keys" {}

variable "private_key_path" {}

variable "ssh_fingerprint" {}

variable "public_key" {}

variable "ansible_user" {}
