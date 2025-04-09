# VideoPrecessorService

# Docker - Para rodar o projeto no docker

$ docker build -t video-processing-service .
$ docker run --rm --env-file .env video-processing-service

# AWS - Criar um repositório e subir o projeto

# 1. Login no ECR
$ aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 8913-7721-3431.dkr.ecr.us-east-1.amazonaws.com

# 2. Criar repositório (uma vez só)
$ aws ecr create-repository --repository-name video-processing-service --region us-east-1

# 3. Build da imagem
$ docker build -t video-processing-service .

# 4. Tag com o caminho completo do ECR
$ docker tag video-processing-service:latest 8913-7721-3431.dkr.ecr.us-east-1.amazonaws.com/video-processing-service:latest

# 5. Push
$ docker push 891377213431.dkr.ecr.us-east-1.amazonaws.com/video-processing-service:latest