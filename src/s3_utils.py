from shlex import quote
import boto3
import os

from src.config import BUCKET_NAME, OUTPUT_PREFIX
from botocore.exceptions import BotoCoreError, ClientError
from tqdm import tqdm
from src.logger import get_logger

s3 = boto3.client("s3")

logger = get_logger(__name__)

class UploadProgress:
    def __init__(self, filename: str):
        self._filename = filename
        self._filesize = float(os.path.getsize(filename))
        self._progress_bar = tqdm(
            total=self._filesize,
            unit='B',
            unit_scale=True,
            unit_divisor=1024,
            desc=os.path.basename(filename),
            ncols=80,
        )

    def __call__(self, bytes_transferred: int):
        self._progress_bar.update(bytes_transferred)

def download_video_from_s3(root_path: str, key: str) -> str:
    
    video_path = os.path.join(root_path, os.path.basename(key))
    
    logger.debug(f"Video salvo em: {video_path}.")
    
    try:
        s3.download_file(BUCKET_NAME, key, video_path)
        logger.debug(f"Download concluido: s3://{BUCKET_NAME}/{key}")  
        return video_path
    except (BotoCoreError, ClientError) as e:
        logger.error(f"Failed to download {key} from S3: {e}")
        raise
    

def upload_zip_to_s3(user_id: str, zip_path: str, original_key: str):
    nome_base = os.path.splitext(os.path.basename(original_key))[0]
    destino_key = f"{OUTPUT_PREFIX}/{nome_base}_{user_id}.zip"
    
    logger.debug(f"Iniciando upload de {zip_path} para s3://{BUCKET_NAME}/{destino_key}")
    
    progress = UploadProgress(zip_path)
    
    try:
        s3.upload_file(
            Filename=zip_path,
            Bucket=BUCKET_NAME,
            Key=destino_key,
            Callback=progress
        )
        
        url_zip_s3 = f"https://{BUCKET_NAME}.s3.amazonaws.com/{quote(destino_key)}"
        
        logger.debug(f"Upload concluido: s3:{url_zip_s3}")
        
        return url_zip_s3
    except (BotoCoreError, ClientError) as e:
        logger.error(f"Erro ao fazer upload para s3://{BUCKET_NAME}/{destino_key}: {e}")
        raise
    