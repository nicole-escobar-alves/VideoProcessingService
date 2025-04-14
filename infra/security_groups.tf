
resource "aws_security_group" "app_sg" {
  name        = "video-mgmt-sg"
  description = "Security Group for Video Processing Service ECS"
  vpc_id      = var.vpc_id

  ingress {
    from_port = 8080
    to_port   = 8080
    protocol  = "tcp"
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
