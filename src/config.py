import os
from dotenv import load_dotenv

load_dotenv()

SQS_URL = os.getenv("SQS_URL")
BUCKET_NAME = os.getenv("BUCKET_NAME")
OUTPUT_PREFIX = os.getenv("OUTPUT_PREFIX", "processed")