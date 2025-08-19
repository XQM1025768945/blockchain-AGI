"""
全球AI脑项目部署脚本

此脚本整合了云部署和GitHub部署功能。
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


def create_github_repo(repo_name, username, token):
    """
    在GitHub上创建仓库
    
    Args:
        repo_name (str): 仓库名称
        username (str): GitHub用户名
        token (str): GitHub个人访问令牌
    """
    print(f"正在创建GitHub仓库: {repo_name}")
    try:
        # 使用GitHub API创建仓库
        subprocess.run([
            "curl", 
            "-u", 
            f"{username}:{token}", 
            "-X", 
            "POST", 
            "-H", 
            "Accept: application/vnd.github.v3+json",
            "https://api.github.com/user/repos",
            "-d", 
            f'{{"name":"{repo_name}","private":false}}'
        ], check=True)
        print("GitHub仓库创建成功")
    except subprocess.CalledProcessError as e:
        print(f"GitHub仓库创建失败: {e}")
        sys.exit(1)


def push_to_github(repo_name, username, token):
    """
    将代码推送到GitHub仓库
    
    Args:
        repo_name (str): 仓库名称
        username (str): GitHub用户名
        token (str): GitHub个人访问令牌
    """
    print(f"正在将代码推送到GitHub仓库: {repo_name}")
    try:
        # 添加远程仓库
        remote_url = f"https://{username}:{token}@github.com/{username}/{repo_name}.git"
        subprocess.run(["git", "remote", "add", "origin", remote_url], check=True)
    except subprocess.CalledProcessError:
        # 如果远程仓库已存在，则更新URL
        subprocess.run(["git", "remote", "set-url", "origin", remote_url], check=True)
    
    # 推送代码
    try:
        subprocess.run(["git", "push", "-u", "origin", "master"], check=True)
        print("代码推送成功")
    except subprocess.CalledProcessError as e:
        print(f"代码推送失败: {e}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="全球AI脑项目部署脚本")
    parser.add_argument("--tag", default="global-brain:latest", help="Docker镜像标签")
    parser.add_argument("--compose-file", default="docker-compose.cloud.yml", help="docker-compose文件路径")
    parser.add_argument("--repo-name", help="GitHub仓库名称")
    parser.add_argument("--username", help="GitHub用户名")
    parser.add_argument("--token", help="GitHub个人访问令牌")
    parser.add_argument("--action", choices=["all", "cloud", "github"], default="all", help="部署动作")
    
    args = parser.parse_args()
    
    # 构建和推送Docker镜像
    if args.action in ["all", "cloud"]:
        build_docker_image(args.tag)
        push_docker_image(args.tag)
    
    # 部署到云服务器
    if args.action in ["all", "cloud"]:
        deploy_to_cloud(args.compose_file)
    
    # 部署到GitHub
    if args.action in ["all", "github"] and args.repo_name and args.username and args.token:
        create_github_repo(args.repo_name, args.username, args.token)
        push_to_github(args.repo_name, args.username, args.token)
    elif args.action == "github" and not (args.repo_name and args.username and args.token):
        print("部署到GitHub需要提供仓库名称、用户名和个人访问令牌")
        sys.exit(1)


if __name__ == "__main__":
    main()