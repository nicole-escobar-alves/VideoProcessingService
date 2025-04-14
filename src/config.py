import os
from dotenv import load_dotenv

load_dotenv()

SQS_UPDATE_URL = os.getenv("SQS_UPDATE_URL")
BUCKET_NAME = os.getenv("BUCKET_NAME")
OUTPUT_PREFIX = os.getenv("OUTPUT_PREFIX", "processed")