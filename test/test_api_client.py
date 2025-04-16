import pytest
from unittest.mock import patch, MagicMock
from requests.exceptions import RequestException
from src.external_service import send_zip

from src.config import VIDEO_MANAGEMENT_URL

def test_send_zip_success(caplog):
    with patch('src.external_service.requests.put') as mock_put:
        # Mock de response com status_code 200 e um json de retorno
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"message": "success"}
        mock_put.return_value = mock_response

        user_id = "user123"
        zip_path = "/tmp/video123.zip"
        video_id = "video123"

        # Executa a função
        send_zip(user_id, zip_path, video_id)

        # Verifica se o PUT foi chamado corretamente
        mock_put.assert_called_once_with(
            f"{VIDEO_MANAGEMENT_URL}/video",
            json={
                'userId': user_id,
                'zipPath': zip_path,
                'videoId': video_id
            },
            headers={'Content-Type': 'application/json'}
        )

        # Verifica se logou o envio
        assert "Enviando atualizacao com payload" in caplog.text


def test_send_zip_failure(caplog):
    with patch('src.external_service.requests.put') as mock_put:
        # Mock de response com erro 500
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = RequestException("Erro 500")  # Exceção correta
        mock_put.return_value = mock_response

        user_id = "user123"
        zip_path = "/tmp/video123.zip"
        video_id = "video123"

        # Executa a função (esperando capturar o erro no log)
        send_zip(user_id, zip_path, video_id)

        # Verifica se logou o erro
        assert "Erro ao enviar ZIP para API" in caplog.text
        
        # Verifica se o mock do requests.put foi chamado corretamente
        mock_put.assert_called_once_with(
            f"{VIDEO_MANAGEMENT_URL}/video", 
            json={'userId': user_id, 'zipPath': zip_path, 'videoId': video_id},
            headers={'Content-Type': 'application/json'}
        )
