subnet_ids                   = ["subnet-02dfefca38889217f", "subnet-064e90a098c98514f"]
vpc_id                       = "vpc-00540ae73d895d3d3"

image_url                    = "561266514983.dkr.ecr.us-east-1.amazonaws.com/video-process-service:3.1"
region                       = "us-east-1"
labsrole_arn                 = "arn:aws:iam::561266514983:role/LabRole"
video_cluster_name           = "video-cluster"
bucket_name                  = "561266514983-video-storage-bucket"
output_prefix                = "processed"
video_uploaded_queue_name    = "video_uploaded"
video_management_url         = "http://internal-shared-alb-1828749500.us-east-1.elb.amazonaws.com/video-management"