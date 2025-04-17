import unittest
from unittest import mock
import asyncio
import json

from src.main import handle_message


class TestHandleMessage(unittest.IsolatedAsyncioTestCase):

    @mock.patch("src.main.logger")
    @mock.patch("src.main.delete_message")
    @mock.patch("src.main.process_message")
    @mock.patch("src.main.sem", new=asyncio.Semaphore(1))
    async def test_handle_message_success(self, mock_process_message, mock_delete_message, mock_logger):
        msg = {
            "Body": json.dumps({
                "video_UrlS3": "s3://mybucket/video.mp4",
                "video_id": "123",
                "user_id": "456"
            }),
            "ReceiptHandle": "abc123",
            "MessageId": "msg789"
        }

        await handle_message(msg)

        mock_process_message.assert_called_once_with("456", "123", "s3://mybucket/video.mp4")
        mock_delete_message.assert_called_once_with("abc123")
        mock_logger.debug.assert_called_with('Mensagem processada e deletada com sucesso.": msg789')

    @mock.patch("src.main.logger")
    @mock.patch("src.main.delete_message")
    @mock.patch("src.main.process_message")
    @mock.patch("src.main.sem", new=asyncio.Semaphore(1))
    async def test_handle_message_error(self, mock_process_message, mock_delete_message, mock_logger):
        mock_process_message.side_effect = Exception("Erro simulado")

        msg = {
            "Body": json.dumps({
                "video_UrlS3": "s3://mybucket/video.mp4",
                "video_id": "123",
                "user_id": "456"
            }),
            "ReceiptHandle": "abc123",
            "MessageId": "msg789"
        }

        await handle_message(msg)

        mock_logger.error.assert_called()
        args, _ = mock_logger.error.call_args
        self.assertIn("Erro ao processar mensagem: Erro simulado", args[0])

        mock_delete_message.assert_not_called()


if __name__ == '__main__':
    unittest.main()
