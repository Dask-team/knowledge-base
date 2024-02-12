#!/bin/bash

# Docker 설치 확인 및 설치
if ! command -v docker &> /dev/null; then
    echo "Docker could not be found. Installing Docker..."
    sudo apt-get update
    sudo apt-get install -y docker
fi

# Docker Compose 설치 확인 및 설치
if ! command -v docker-compose &> /dev/null; then
    echo "Docker Compose could not be found. Installing Docker Compose..."
    sudo apt-get update
    sudo apt-get install -y docker-compose
fi

# Docker 서비스 시작
# sudo systemctl start docker

# Docker Compose 실행
echo "Starting Elasticsearch with Nori, Kuromoji, and English analyzers..."
sudo docker-compose up -d
