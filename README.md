# VideoPrecessorService

# Docker - Para rodar o projeto no docker

$ docker build -t video-processing-service .
$ docker run --rm --env-file .env video-processing-service

# Kubernets - Para rodar o projeto no kubernet

$ aws eks --region <região> update-kubeconfig --name <nome-do-cluster>

Isso vai adicionar a configuração necessária no arquivo ~/.kube/config para que você consiga interagir com o EKS usando o kubectl.

Dentro da pasta k8s/ :

$ cd k8s
$ kubectl kustomize .

# AWS - Criar um repositório e subir o projeto

# 1. Login no ECR
$ aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 891377213431.dkr.ecr.us-east-1.amazonaws.com

# 2. Criar repositório (uma vez só)
$ aws ecr create-repository --repository-name video-processing-service --region us-east-1

# 3. Build da imagem
$ docker build -t video-processing-service .

# 4. Tag com o caminho completo do ECR
$ docker tag video-processing-service:latest 891377213431.dkr.ecr.us-east-1.amazonaws.com/video-processing-service:latest

# 5. Push
$ docker push 891377213431.dkr.ecr.us-east-1.amazonaws.com/video-processing-service:latest

# Para rodar o teste

Na raíz do projeto rodar

$ python -m pytest

# Gerar relatório pytest

$ pip install pytest pytest-cov

$ python -m pytest --cov=src --cov-report=xml