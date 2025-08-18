# 全球脑大模型 Dockerfile

# 使用Python 3.9作为基础镜像
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 复制项目文件
COPY . .

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

# 创建必要的目录
RUN mkdir -p model install temp logs knowledge_base/data

# 暴露端口（用于网络服务，如果需要的话）
EXPOSE 8888

# 设置环境变量
ENV BITTENSOR_API_KEY=your_api_key_here
ENV ENCRYPTION_KEY=default_key_32_bytes_long!!

# 启动主程序
CMD ["python", "main.py"]