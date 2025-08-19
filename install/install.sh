#!/bin/bash

# 安装脚本

echo "安装区块链模型..."

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

echo "安装完成!"