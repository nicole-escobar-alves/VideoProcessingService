import boto3
from src.config import SQS_URL

sqs = boto3.client("sqs")

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