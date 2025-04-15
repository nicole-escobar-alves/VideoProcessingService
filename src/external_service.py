import requests
from src.logger import get_logger
from src.config import VIDEO_MANAGEMENT_URL
logger = get_logger(__name__)

url = f"{VIDEO_MANAGEMENT_URL}/video"

def send_zip(user_id: str, zip_path: str, video_id: str):
    
    payload = {
        'userId': user_id,
        'zipPath': zip_path, 
        'videoId': video_id
    }
    headers = {
        'Content-Type': 'application/json'
    }
 
    try:
        logger.info(f'Enviando atualizacao com payload: {payload}')
        
        response = requests.put(url, json=payload, headers=headers)
        response.raise_for_status()  # Levanta exceção automática se não for 2xx

        logger.debug(f"Resposta: {response.json()}.")

    except requests.exceptions.RequestException as e:
        logger.error(f"Erro ao enviar ZIP para API: {e}")