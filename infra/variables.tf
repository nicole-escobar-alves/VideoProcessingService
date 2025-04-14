variable "subnet_ids" {
  type = list(string)
}
variable "vpc_id" {}
variable "image_url" {}
variable "region" {}
variable "spring_profile" {}
variable "dynamo_table" {}
variable "video_uploaded_queue_name" {}
variable "notification_queue_name" {}
variable "labsrole_arn" {}
variable "video_cluster_name" {}
variable "bucket_name" {}
variable "output_prefix" {}

variable "AWS_ACCESS_KEY_ID" {}
variable "AWS_SECRET_ACCESS_KEY" {}
variable "AWS_SESSION_TOKEN" {}

