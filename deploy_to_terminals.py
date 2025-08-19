"""
在网络终端设备中部署区块链模型的脚本

此脚本将模型文件和必要的依赖部署到网络终端设备。
"""

import os
import sys
import subprocess
import argparse
import shutil


def deploy_to_terminal(target_path, model_path="./model/model.pt", install_path="./install"):
    """
    将模型和安装文件部署到终端设备
    
    Args:
        target_path (str): 终端设备的目标路径
        model_path (str): 模型文件路径
        install_path (str): 安装文件路径
    """
    print(f"正在将模型部署到终端设备: {target_path}")
    
    # 创建目标目录
    os.makedirs(target_path, exist_ok=True)
    
    # 复制模型文件
    if os.path.exists(model_path):
        # 创建model子目录
        model_dir = os.path.join(target_path, "model")
        os.makedirs(model_dir, exist_ok=True)
        target_model_path = os.path.join(model_dir, "model.pt")
        shutil.copy2(model_path, target_model_path)
        print(f"模型文件已复制到: {target_model_path}")
    else:
        print(f"警告: 模型文件不存在: {model_path}")
    
    # 复制安装文件
    if os.path.exists(install_path):
        target_install_path = os.path.join(target_path, "install")
        if os.path.exists(target_install_path):
            shutil.rmtree(target_install_path)
        shutil.copytree(install_path, target_install_path)
        print(f"安装文件已复制到: {target_install_path}")
    else:
        print(f"警告: 安装文件目录不存在: {install_path}")
    
    # 创建启动脚本
    startup_script = os.path.join(target_path, "start_terminal.sh")
    with open(startup_script, "w") as f:
        f.write("""#!/bin/bash
# 终端设备启动脚本

cd $(dirname $0)

# 激活Python虚拟环境（如果存在）
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# 安装依赖
if [ -f "install/requirements.txt" ]; then
    pip install -r install/requirements.txt
fi

# 启动终端节点
python -m demos.terminal_node
""")
    
    # 给启动脚本添加执行权限
    os.chmod(startup_script, 0o755)
    print(f"启动脚本已创建: {startup_script}")
    
    print("终端设备部署完成")


def main():
    parser = argparse.ArgumentParser(description="在网络终端设备中部署区块链模型")
    parser.add_argument("--target-path", required=True, help="终端设备的目标路径")
    parser.add_argument("--model-path", default="./model/model.pt", help="模型文件路径")
    parser.add_argument("--install-path", default="./install", help="安装文件路径")
    
    args = parser.parse_args()
    
    # 部署到终端设备
    deploy_to_terminal(args.target_path, args.model_path, args.install_path)


if __name__ == "__main__":
    main()