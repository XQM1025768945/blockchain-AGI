"""
将全球AI脑项目部署到云服务器的脚本

此脚本将构建Docker镜像并推送到Docker Hub，然后使用docker-compose在云服务器上部署服务。
"""

import os
import sys
import subprocess
import argparse


def build_docker_image(tag):
    """
    构建Docker镜像
    
    Args:
        tag (str): 镜像标签
    """
    print(f"正在构建Docker镜像: {tag}")
    try:
        subprocess.run(["docker", "build", "-t", tag, "."], check=True)
        print("Docker镜像构建成功")
    except subprocess.CalledProcessError as e:
        print(f"Docker镜像构建失败: {e}")
        sys.exit(1)


def push_docker_image(tag):
    """
    推送Docker镜像到Docker Hub
    
    Args:
        tag (str): 镜像标签
    """
    print(f"正在推送Docker镜像到Docker Hub: {tag}")
    try:
        subprocess.run(["docker", "push", tag], check=True)
        print("Docker镜像推送成功")
    except subprocess.CalledProcessError as e:
        print(f"Docker镜像推送失败: {e}")
        sys.exit(1)


def deploy_to_cloud(compose_file):
    """
    使用docker-compose在云服务器上部署服务
    
    Args:
        compose_file (str): docker-compose文件路径
    """
    print(f"正在使用docker-compose部署服务: {compose_file}")
    try:
        subprocess.run(["docker-compose", "-f", compose_file, "up", "-d"], check=True)
        print("服务部署成功")
    except subprocess.CalledProcessError as e:
        print(f"服务部署失败: {e}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="将全球AI脑项目部署到云服务器")
    parser.add_argument("--tag", default="global-brain:latest", help="Docker镜像标签")
    parser.add_argument("--compose-file", default="docker-compose.cloud.yml", help="docker-compose文件路径")
    
    args = parser.parse_args()
    
    # 构建Docker镜像
    build_docker_image(args.tag)
    
    # 推送Docker镜像到Docker Hub
    push_docker_image(args.tag)
    
    # 部署到云服务器
    deploy_to_cloud(args.compose_file)


if __name__ == "__main__":
    main()