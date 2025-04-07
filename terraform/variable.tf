variable "access_key" {
  description = "Aws access key"
  type        = string
  default     = ""
}
variable "secret_key" {
  description = "Aws secret key"
  type        = string
  default     = ""
}
variable "account_id" {
  description = "Aws account id"
  type        = string
  default     = "891377213431"
}
variable "session_token" {
  description = "Aws session token"
  type        = string
  default     = ""
}
variable "aws_region" {
  description = "Região dos recursos"
  type        = string
  default     = "us-east-1"
}

variable "opencv_layer_arn" {
  description = "ARN da layer com OpenCV"
  default     = "arn:aws:lambda:us-east-1:339712794784:layer:opencv-python:10"
}

variable "project_name" {
  description = "Nome do projeto"
  default     = "hackathon-fiap"
}
