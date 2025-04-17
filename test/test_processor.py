import os
import cv2
import tempfile
import zipfile
import numpy as np
import pytest
from src.processor import extract_frames_to_zip

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