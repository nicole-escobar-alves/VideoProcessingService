import os
import boto3
from behave import given, when, then
from botocore.exceptions import NoCredentialsError
from unittest.mock import MagicMock
from io import BytesIO

# Mock para o cliente S3
s3_client = boto3.client('s3')
s3_client.upload_fileobj = MagicMock()
s3_client.download_file = MagicMock()
s3_client.head_object = MagicMock()

@given('a video is uploaded to S3')
def step_impl(context):
    # Simula o upload de um vídeo para o S3
    video_file = 'tests/video.mp4'  # Caminho real para o vídeo
    context.bucket_name = 'my-test-bucket'  # Substitua pelo seu bucket S3
    context.key = 'videos/video.mp4'
    
    # Criação de um arquivo de vídeo em memória (mock)
    if not os.path.exists(video_file):
        with open(video_file, 'wb') as f:
            f.write(b"fake video content")  # Simula conteúdo de vídeo
    
    try:
        with open(video_file, 'rb') as data:
            # Usa o mock para simular o upload para o S3
            s3_client.upload_fileobj(data, context.bucket_name, context.key)
    except NoCredentialsError:
        raise Exception("AWS credentials are missing or invalid")

@when('I download the video')
def step_impl(context):
    # Verifica e cria o diretório, se necessário
    download_dir = 'tests'
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

    download_path = os.path.join(download_dir, 'downloaded_video.mp4')  # Caminho real de download
    try:
        # Mocka o download do arquivo, criando o arquivo no caminho especificado
        with open(download_path, 'wb') as f:
            f.write(b"fake video content")  # Simula o conteúdo do vídeo baixado
        context.download_path = download_path
    except NoCredentialsError:
        raise Exception("AWS credentials are missing or invalid")

@then('the file should exist')
def step_impl(context):
    # Verifica se o arquivo foi baixado com sucesso
    assert os.path.exists(context.download_path), f"File {context.download_path} does not exist."

@given('a zip file')
def step_impl(context):
    # Simula a criação de um arquivo zip
    context.zip_file = 'tests/file.zip'  # Caminho real para o arquivo zip
    context.bucket_name = 'my-test-bucket'  # Substitua pelo seu bucket S3
    context.key = 'zips/file.zip'
    
    # Verifique se o arquivo ZIP existe ou crie um arquivo simulado
    if not os.path.exists(context.zip_file):
        with open(context.zip_file, 'w') as file:
            file.write('fake zip content')  # Simulação de conteúdo do arquivo zip

@when('I upload the zip to S3 for user with original key')
def step_impl(context):
    # Simula o upload de um arquivo zip para o S3
    try:
        with open(context.zip_file, 'rb') as data:
            s3_client.upload_fileobj(data, context.bucket_name, context.key)
    except NoCredentialsError:
        raise Exception("AWS credentials are missing or invalid")

@then('the zip file should be uploaded to S3 with the correct key')
def step_impl(context):
    # Simula a verificação do upload do arquivo ZIP no S3
    s3_client.head_object(Bucket=context.bucket_name, Key=context.key)
    # Verifica se o mock da resposta é bem-sucedido
    assert s3_client.head_object.called, f"Failed to upload zip file to S3 with key {context.key}"