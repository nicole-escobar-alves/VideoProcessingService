FROM python:3.11.9-slim

WORKDIR /app

# Instala ffmpeg e libs necessárias para OpenCV
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONPATH="/app"

CMD ["python", "main.py"]