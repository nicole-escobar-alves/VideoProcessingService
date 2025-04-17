import boto3
import pytest
from moto import mock_aws
import os

from src import sqs_worker

@mock_sqs
def test_receive_message_returns_messages():
    # Configura o mock SQS
    sqs = boto3.client("sqs", region_name="us-east-1")
    queue = sqs.create_queue(QueueName="test-queue")
    queue_url = queue["QueueUrl"]

    # Envia mensagens para a fila mockada
    sqs.send_message(QueueUrl=queue_url, MessageBody="message 1")
    sqs.send_message(QueueUrl=queue_url, MessageBody="message 2")

    # Injeta o SQS fake no módulo e a URL da fila mockada
    sqs_worker.sqs = sqs
    sqs_worker.SQS_UPDATE_URL = queue_url

    # Executa a função
    messages = sqs_worker.receive_message()

    # Valida as mensagens retornadas
    assert len(messages) == 2
    assert messages[0]["Body"] == "message 1"
    assert messages[1]["Body"] == "message 2"


@mock_sqs
def test_receive_message_no_messages():
    # Configura o mock SQS
    sqs = boto3.client("sqs", region_name="us-east-1")
    queue = sqs.create_queue(QueueName="test-queue")
    queue_url = queue["QueueUrl"]

    # Injeta o SQS fake no módulo e a URL da fila mockada
    sqs_worker.sqs = sqs
    sqs_worker.SQS_UPDATE_URL = queue_url

    # Executa a função sem mensagens
    messages = sqs_worker.receive_message()

    # Valida retorno vazio
    assert messages == []


@mock_sqs
def test_delete_message():
    # Configura o mock SQS
    sqs = boto3.client("sqs", region_name="us-east-1")
    queue = sqs.create_queue(QueueName="test-queue")
    queue_url = queue["QueueUrl"]

    # Envia uma mensagem e captura seu receipt handle
    response = sqs.send_message(QueueUrl=queue_url, MessageBody="to delete")
    receipt_handle = sqs.receive_message(QueueUrl=queue_url)["Messages"][0]["ReceiptHandle"]

    # Injeta o SQS fake no módulo e a URL da fila mockada
    sqs_worker.sqs = sqs
    sqs_worker.SQS_UPDATE_URL = queue_url

    # Deleta a mensagem
    sqs_worker.delete_message(receipt_handle)

    # Verifica que a fila está vazia após deleção
    messages_after_delete = sqs.receive_message(QueueUrl=queue_url)
    assert "Messages" not in messages_after_delete
