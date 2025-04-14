resource "aws_cloudwatch_log_group" "ecs_video_management" {
  name              = "/ecs/video-processing-service"
  retention_in_days = 7
}
