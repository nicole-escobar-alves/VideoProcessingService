import requests
from src.logger import get_logger

logger = get_logger(__name__)

url = ''

def send_zip(user_id: str, zip_path: str, video_id: str):
    
    payload = {
        'user_id': user_id,
        'zip_UrlS3': zip_path, 
        'video_id': video_id
    }
    
    headers = {
        'Content-Type': 'application/json'
    }
 
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # Levanta exceção automática se não for 2xx

        logger.debug(f"Resposta: {response.json()}.")

    except requests.exceptions.RequestException as e:
        logger.error(f"Erro ao enviar ZIP para API: {e}")