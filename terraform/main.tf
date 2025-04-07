provider "aws" {
  region     = var.aws_region
  access_key = var.access_key
  secret_key = var.secret_key
  token      = var.session_token
}

resource "aws_sqs_queue" "video_queue" {
  name                       = "video-upload-queue"
  visibility_timeout_seconds = 60
  fifo_queue                 = false
}

module "bucket" {
  source       = "./modules/bucket-s3"
  project_name = var.project_name
}
