terraform {
  required_version = ">= 1.3.0"

  backend "s3" {
    bucket = "561266514983-terraform-state-fiapx"
    key    = "infra-ecs-video-processing-service/terraform.tfstate"
    region = "us-east-1"
  }
}

provider "aws" {
  region = "us-east-1"
}
