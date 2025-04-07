# Ponto de entrada real
import asyncio
import json
import os
import shutil

from src.sqs_worker import receive_message, delete_message
from src.s3_utils import download_video_from_s3, upload_zip_to_s3
from src.processor import extract_frames_to_zip, sanitize_video

CONCURRENCY_LIMIT = 5
sem = asyncio.Semaphore(CONCURRENCY_LIMIT)

def process_message(user_id: str, video_s3_key: str):
    
    print(f"Processando vídeo: {video_s3_key}")
    
    root_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "VideosFolder", user_id)
    os.makedirs(root_dir, exist_ok=True)
    
    try:
        video_path = download_video_from_s3(root_dir, video_s3_key)
        print(f"[DEBUG] Vídeo salvo em: {video_path}")
        # Sanitize antes de extrair os frames
        sanitized_path = os.path.join(root_dir, "sanitized_" + os.path.basename(video_path))
        sanitize_video(video_path, sanitized_path)

        zip_path = extract_frames_to_zip(user_id, root_dir, sanitized_path)
        upload_zip_to_s3(user_id, zip_path, video_s3_key)
        
        if os.path.isdir(root_dir):
            shutil.rmtree(root_dir)
            print("Pasta deletada com sucesso.")
        else:
            print("Pasta não encontrada.")
            
        print(f"Processado com sucesso: {video_s3_key}")
    except Exception as e:
        print(f"[ERROR] Erro ao processar vídeo: {e}")

async def handle_message(msg):
    async with sem:
        try:
            corpo = json.loads(msg["Body"])
            video_key = corpo["video_UrlS3"]
            user_id = str(corpo["user_id"])

            await asyncio.to_thread(process_message, user_id, video_key)
            await asyncio.to_thread(delete_message, msg["ReceiptHandle"])
            print("Mensagem processada e deletada com sucesso.")
        except Exception as e:
            print(f"[ERROR] Erro ao processar mensagem: {e}")
        
async def worker_loop():
    
    print("Worker iniciado. Aguardando mensagens...")
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

def main():
    asyncio.run(worker_loop())