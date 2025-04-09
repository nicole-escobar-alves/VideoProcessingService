import os
import boto3
from src.config import SQS_URL

region = os.environ.get("AWS_REGION", "us-east-1")
sqs = boto3.client("sqs", region_name=region)

def receive_message():
    response = sqs.receive_message(
        QueueUrl=SQS_URL,
        MaxNumberOfMessages=5,
        WaitTimeSeconds=10,
        VisibilityTimeout=30
    )
    return response.get("Messages", [])

def delete_message(receipt_handle):
    sqs.delete_message(
        QueueUrl=SQS_URL,
        ReceiptHandle=receipt_handle
    )