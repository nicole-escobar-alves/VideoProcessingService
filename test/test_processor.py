import os
import cv2
import tempfile
import zipfile
import numpy as np
import pytest
from src.processor import extract_frames_to_zip
import subprocess
import unittest
from unittest import mock
from zipfile import ZipFile

def create_dummy_video(path, frame_count=50, width=640, height=480, fps=30):
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(path, fourcc, fps, (width, height))
    for _ in range(frame_count):
        frame = np.random.randint(0, 255, (height, width, 3), dtype=np.uint8)
        out.write(frame)
    out.release()

def test_extract_frames_to_zip():
    with tempfile.TemporaryDirectory() as tmpdir:
        video_path = os.path.join(tmpdir, "test_video.avi")
        create_dummy_video(video_path)

        video_id = "test_video"
        root_path = tmpdir
        video_s3_path = video_path

        zip_path = extract_frames_to_zip(video_id, root_path, video_s3_path)

        # Verificar se o arquivo zip foi criado
        assert os.path.isfile(zip_path), "Arquivo zip não foi criado."

        # Verificar conteúdo do zip
        with zipfile.ZipFile(zip_path, 'r') as zipf:
            file_list = zipf.namelist()
            assert len(file_list) > 0, "Nenhum frame foi extraído para o zip."
            
            # Checar se os arquivos têm o padrão esperado
            for filename in file_list:
                assert filename.startswith("frame_") and filename.endswith(".jpg")

        print(f"Teste passou. {len(file_list)} frames extraídos e zipados.")

if __name__ == "__main__":
    pytest.main([__file__])
    
class TestExtractFramesToZip(unittest.TestCase):

    @mock.patch("os.makedirs")
    @mock.patch("cv2.resize")
    @mock.patch("cv2.imwrite")
    @mock.patch("os.listdir")
    @mock.patch("cv2.VideoCapture")
    def test_extract_frames_success(self, mock_VideoCapture, mock_listdir, mock_imwrite, mock_resize, mock_makedirs):
        video_id = "test_video"
        root_path = "temp"
        video_s3_path = "/fake/path/to/video.mp4"

        # Mock do VideoCapture
        mock_cap_instance = mock.Mock()
        mock_VideoCapture.return_value = mock_cap_instance
        mock_cap_instance.isOpened.return_value = True

        frame_mock = mock.Mock()
        # Simula 3 frames lidos e depois fim
        mock_cap_instance.read.side_effect = [
            (True, frame_mock), (True, frame_mock), (True, frame_mock), (False, None)
        ]

        # Mock da listagem de arquivos extraídos
        mock_listdir.return_value = ["frame_0000.jpg", "frame_0010.jpg", "frame_0020.jpg"]

        # Executa a função
        zip_path = extract_frames_to_zip(video_id, root_path, video_s3_path)

        frames_dir = os.path.join(root_path, f"{video_id}_frames")
        expected_zip_path = os.path.join(root_path, f"{video_id}_frames.zip")

        # Verificações
        mock_makedirs.assert_called_once_with(frames_dir, exist_ok=True)
        self.assertEqual(zip_path, expected_zip_path)

        # Só o frame 0 deve passar pelo if frame_count % 10 == 0
        self.assertEqual(mock_resize.call_count, 1)
        self.assertEqual(mock_imwrite.call_count, 1)

        # Verifica se os arquivos foram adicionados ao zip
        with ZipFile(zip_path, 'r') as zipf:
            zipped_files = zipf.namelist()
            self.assertEqual(set(zipped_files), set(mock_listdir.return_value))

    @mock.patch("cv2.VideoCapture")
    def test_extract_frames_video_not_opened(self, mock_VideoCapture):
        video_id = "test_video"
        root_path = "temp"
        video_s3_path = "/fake/path/to/video.mp4"

        mock_VideoCapture.return_value.isOpened.return_value = False

        with self.assertRaises(ValueError) as context:
            extract_frames_to_zip(video_id, root_path, video_s3_path)

        self.assertIn(f"Falha ao abrir vídeo: {video_s3_path}", str(context.exception))

    @mock.patch("cv2.VideoCapture")
    def test_extract_frames_subprocess_error_handling(self, mock_VideoCapture):
        video_id = "test_video"
        root_path = "temp"
        video_s3_path = "/fake/path/to/video.mp4"

        mock_cap_instance = mock.Mock()
        mock_VideoCapture.return_value = mock_cap_instance
        mock_cap_instance.isOpened.return_value = True

        # Esse erro não ocorre em cap.read(), mas para testar o except
        def raise_error():
            raise subprocess.CalledProcessError(1, "fake_cmd")

        mock_cap_instance.read.side_effect = raise_error

        with self.assertRaises(subprocess.CalledProcessError):
            extract_frames_to_zip(video_id, root_path, video_s3_path)


if __name__ == '__main__':
    unittest.main()
