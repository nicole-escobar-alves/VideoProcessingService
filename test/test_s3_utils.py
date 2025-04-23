import os
import tempfile
from moto.s3 import mock_s3
import boto3
from unittest.mock import patch, MagicMock
from botocore.exceptions import ClientError
import pytest

from src.s3_utils import download_video_from_s3, upload_zip_to_s3
from src.config import BUCKET_NAME, OUTPUT_PREFIX

#@mock_aws
@mock_s3
def test_download_video_from_s3():
    
    # Cria o mock do cliente S3
    s3 = boto3.client("s3", region_name="us-east-1")
    # Cria um bucket fake
    s3.create_bucket(Bucket=BUCKET_NAME)
    
    video_key = "videos/video123.mp4"
    s3.put_object(Bucket=BUCKET_NAME, Key=video_key, Body=b"fake video content")
    
    root_path = tempfile.gettempdir()
    video_id = "1"
    
    expected_path = os.path.join(root_path, os.path.basename(video_id)) 
    
    from src import s3_utils
    s3_utils.s3 = s3
    
    result = download_video_from_s3(root_path, video_id, video_key)
    
    assert os.path.exists(result)
    assert open(result, "rb").read() == b"fake video content"
    assert result == expected_path
    
@mock_s3
def test_upload_zip_to_s3_success():
    # Configuração do mock S3
    s3 = boto3.client("s3", region_name="us-east-1")
    s3.create_bucket(Bucket=BUCKET_NAME)
    
    # Caminho do arquivo zip (criando um arquivo temporário para o teste)
    zip_path = "/tmp/test_video.zip"
    os.makedirs(os.path.dirname(zip_path), exist_ok=True)
    
    with open(zip_path, "wb") as f:
        f.write(b"fake zip content")  # Conteúdo fake para o arquivo zip

    # Parametrizando outros valores necessários
    user_id = "user123"
    video_id = "video123"
    original_key = "videos/video123.mp4"

    # Chamando a função a ser testada
    result_url = upload_zip_to_s3(user_id, video_id, zip_path, original_key)
    
    # Verificando se a URL gerada está correta
    expected_url = f"{OUTPUT_PREFIX}/{user_id}/{os.path.splitext(os.path.basename(original_key))[0]}_{video_id}.zip"
    assert result_url == expected_url

    # Verificando se o arquivo foi realmente enviado para o mock S3
    response = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix=f"{OUTPUT_PREFIX}/{user_id}/")
    assert response["KeyCount"] == 1
    assert response["Contents"][0]["Key"] == f"{OUTPUT_PREFIX}/{user_id}/{os.path.splitext(os.path.basename(original_key))[0]}_{video_id}.zip"
    
    # Limpeza após o teste
    os.remove(zip_path)
    
@mock_s3
def test_upload_zip_to_s3_file_not_found():
    # Mock para o S3
    s3 = boto3.client("s3", region_name="us-east-1")
    s3.create_bucket(Bucket=BUCKET_NAME)
    
    # Testando quando o arquivo zip não existe
    zip_path = "/tmp/non_existing_file.zip"
    user_id = "user123"
    video_id = "video123"
    original_key = "videos/video123.mp4"
    
    with pytest.raises(FileNotFoundError):
        upload_zip_to_s3(user_id, video_id, zip_path, original_key)
    
      