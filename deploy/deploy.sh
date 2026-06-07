#!/bin/bash
set -e

echo "========================================="
echo "  全球神经网络大脑 —— 原型一键部署"
echo "========================================="

cd "$(dirname "$0")/.."

echo "[1/3] 停止旧服务..."
docker-compose down

echo "[2/3] 构建并启动服务..."
docker-compose up -d --build

echo "[3/3] 服务已就绪"
echo "  - AI 编排器:    http://localhost:8000"
echo "  - AIP 接口文档: http://localhost:8000/docs"
echo "  - 脉冲 WebSocket: ws://localhost:8000/ws/spike"
