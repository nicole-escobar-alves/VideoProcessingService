data "aws_sqs_queue" "video_uploaded" {
  name = var.video_uploaded_queue_name
}

data "aws_sqs_queue" "notification" {
  name = var.notification_queue_name
}

data "aws_ecs_cluster" "video_cluster" {
  cluster_name = var.video_cluster_name
}
