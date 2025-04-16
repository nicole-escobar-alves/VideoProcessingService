# Ponto de entrada real
import asyncio
import json
import os
import shutil

from src.sqs_worker import receive_message, delete_message
from src.s3_utils import download_video_from_s3, upload_zip_to_s3
from src.processor import extract_frames_to_zip, sanitize_video
from src.external_service import send_zip
from src.logger import get_logger

CONCURRENCY_LIMIT = 5
sem = asyncio.Semaphore(CONCURRENCY_LIMIT)

logger = get_logger(__name__)

def process_message(user_id: str, video_id: str, video_s3_key: str):
    
    logger.debug(f"Processando vídeo do s3: {video_s3_key}")
    
    root_dir = os.path.join("/tmp", "VideosFolder", user_id)
    os.makedirs(root_dir, exist_ok=True)
    
    try:
        video_path = download_video_from_s3(root_dir, video_id, video_s3_key)
        
        sanitized_path = os.path.join(root_dir, "sanitized_" + os.path.basename(video_path) + ".mp4")
        sanitize_video(video_path, sanitized_path)
    
        zip_path = extract_frames_to_zip(video_id, root_dir, sanitized_path)
    
        destino_key = upload_zip_to_s3(user_id, video_id, zip_path, video_s3_key)
        
        send_zip(user_id, destino_key, video_id)
           
        logger.info(f"Processamento do vídeo {video_id} concluído com sucesso.")
        
    except Exception as e:
        logger.error(f"Erro no processamento do vídeo {video_id}: {e}")
    
    finally:
       delete_folder(root_dir)
    
    

def delete_folder(root_dir: str):
    try:     
        if os.path.isdir(root_dir):
            shutil.rmtree(root_dir)
            logger.debug(f"Pasta deletada com sucesso: {root_dir}")
        else:
            logger.warning(f"Pasta não encontrada: {root_dir}")
    except Exception as e:
        logger.error(f"Erro ao tentar deletar as pastas criadas: {e}")
    

async def handle_message(msg):
    async with sem:
        try:
            corpo = json.loads(msg["Body"])
            video_key = corpo["video_UrlS3"]
            video_id = str(corpo["video_id"])
            user_id = str(corpo["user_id"])

            await asyncio.to_thread(process_message, user_id, video_id, video_key)
            await asyncio.to_thread(delete_message, msg["ReceiptHandle"])
            logger.debug(f'Mensagem processada e deletada com sucesso.": {msg["MessageId"]}')
            
            
        except Exception as e:
            logger.error(f"Erro ao processar mensagem: {e}")
        
async def worker_loop():
    
    logger.debug("Worker iniciado. Aguardando mensagens...")
    
    while True:
        mensagens = await asyncio.to_thread(receive_message)
        if not mensagens:
            await asyncio.sleep(2)
            continue
        
        # Cria tasks individuais para cada mensagem
        tasks = [asyncio.create_task(handle_message(msg)) for msg in mensagens]

        # Roda tudo em paralelo e espera terminar
        await asyncio.gather(*tasks)

        await asyncio.sleep(1)

async def main():
    await worker_loop()