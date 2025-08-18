"""
将全球AI脑项目部署到GitHub的脚本

此脚本将项目推送到GitHub仓库。
"""

import os
import sys
import subprocess
import argparse


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
    parser = argparse.ArgumentParser(description="将全球AI脑项目部署到GitHub")
    parser.add_argument("--repo-name", required=True, help="GitHub仓库名称")
    parser.add_argument("--username", required=True, help="GitHub用户名")
    parser.add_argument("--token", required=True, help="GitHub个人访问令牌")
    
    args = parser.parse_args()
    
    # 创建GitHub仓库
    create_github_repo(args.repo_name, args.username, args.token)
    
    # 推送代码到GitHub
    push_to_github(args.repo_name, args.username, args.token)


if __name__ == "__main__":
    main()