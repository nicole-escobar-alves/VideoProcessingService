import os
import cv2
from zipfile import ZipFile
import subprocess

def sanitize_video(input_path: str, output_path: str) -> None:
    """
    Reencoda o vídeo removendo áudio, legendas e metadados extras.
    Salva um novo arquivo limpo no output_path.
    """
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
        print(f"Vídeo sanitizado e salvo em: {output_path}")
        return output_path
    
    except subprocess.CalledProcessError as e:
        print("[ERROR] Erro ao sanitizar vídeo:", e.stderr.decode())
        
def extract_frames_to_zip(user_id: str, root_path: str, video_s3_path: str) -> str:

    cap = cv2.VideoCapture(video_s3_path)
    frame_count = 0
    
    frames_dir = os.path.join(root_path, f"{user_id}_frames")
    os.makedirs(frames_dir, exist_ok=True)
    
    print("FRAMES_PATH: " + frames_dir)
    frame_skip = 10
    scale = 0.5
    quality_weight = 70
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        if frame_count % frame_skip == 0:
            frame_path = os.path.join(frames_dir, f"frame_{frame_count:04d}.jpg")
            resized = cv2.resize(frame, (0, 0), fx=scale, fy=scale)
            cv2.imwrite(frame_path, resized, [int(cv2.IMWRITE_JPEG_QUALITY), quality_weight])
        frame_count += 1

    cap.release()
    print("Frames extraídos.")
    zip_path = os.path.join(root_path, f"{user_id}_frames.zip")
    with ZipFile(zip_path, 'w') as zipf:
        for filename in os.listdir(frames_dir):
            full_path = os.path.join(frames_dir, filename)
            zipf.write(full_path, arcname=filename)
    print(f'Pasta zip criada no caminho: {zip_path}')
    return zip_path