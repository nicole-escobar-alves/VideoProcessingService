import os
import cv2
import subprocess

from src.logger import get_logger
from zipfile import ZipFile

logger = get_logger(__name__)

def sanitize_video(input_path: str, output_path: str) -> None:

    command = [
        "ffmpeg",
        "-y",                  # sobrescreve o arquivo de saída sem perguntar
        "-i", input_path,      # arquivo de entrada
        "-an",                 # remove o áudio
        "-vcodec", "libx264",  # codec de vídeo
        "-pix_fmt", "yuv420p", # formato de cor compatível com OpenCV
        output_path
    ]

    try:
        subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        logger.debug(f"Vídeo sanitizado e salvo em: {output_path}")
        
        return output_path
    
    except subprocess.CalledProcessError as e:
        logger.error("Erro ao sanitizar vídeo:", e.stderr.decode())
        
def extract_frames_to_zip(video_id: str, root_path: str, video_s3_path: str) -> str:

    cap = cv2.VideoCapture(video_s3_path)
    
    if not cap.isOpened():
        logger.error(f"Não foi possível abrir o vídeo: {video_s3_path}")
        raise ValueError(f"Falha ao abrir vídeo: {video_s3_path}")
    
    frame_count = 0
    extracted_count = 0
    
    frames_dir = os.path.join(root_path, f"{video_id}_frames")
    os.makedirs(frames_dir, exist_ok=True)
    
    frame_skip = 10
    scale = 0.5
    quality_weight = 70
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            if frame_count % frame_skip == 0:
                frame_path = os.path.join(frames_dir, f"frame_{frame_count:04d}.jpg")
                resized = cv2.resize(frame, (0, 0), fx=scale, fy=scale)
                cv2.imwrite(frame_path, resized, [int(cv2.IMWRITE_JPEG_QUALITY), quality_weight])
                extracted_count += 1
                
            frame_count += 1
        
        logger.debug(f"{extracted_count} frames extraídos de {frame_count} frames totais.")

        zip_path = os.path.join(root_path, f"{video_id}_frames.zip")
        
        with ZipFile(zip_path, 'w') as zipf:
            for filename in os.listdir(frames_dir):
                full_path = os.path.join(frames_dir, filename)
                zipf.write(full_path, arcname=filename)
        
        logger.debug(f"Pasta zip criada no caminho: {zip_path}.")
        
        return zip_path
        
    except subprocess.CalledProcessError as e:
        logger.error(f"Erro ao processar vídeo {video_id}: {e}")
        raise
    
    finally:
        cap.release()
    
