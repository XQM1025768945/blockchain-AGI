"""
测试网络终端设备部署功能的脚本
"""

import os
import sys
import subprocess
import tempfile
import shutil

def test_terminal_deployment():
    """
    测试终端设备部署功能
    """
    print("开始测试终端设备部署功能...")
    
    # 创建临时目录作为目标设备
    target_path = tempfile.mkdtemp(prefix="agi_test_")
    print(f"创建临时目标目录: {target_path}")
    
    try:
        # 运行部署脚本
        deploy_script = os.path.join(os.path.dirname(__file__), "deploy_to_terminals.py")
        cmd = [sys.executable, deploy_script, "--target-path", target_path]
        print(f"运行部署脚本: {' '.join(cmd)}")
        
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=os.path.dirname(__file__))
        
        print("部署脚本输出:")
        print(result.stdout)
        if result.stderr:
            print("部署脚本错误输出:")
            print(result.stderr)
        
        if result.returncode != 0:
            print(f"部署脚本执行失败，返回码: {result.returncode}")
            return False
        
        # 检查目标目录中的文件
        print("检查目标目录中的文件...")
        for root, dirs, files in os.walk(target_path):
            level = root.replace(target_path, '').count(os.sep)
            indent = ' ' * 2 * level
            print(f'{indent}{os.path.basename(root)}/')
            subindent = ' ' * 2 * (level + 1)
            for file in files:
                print(f'{subindent}{file}')
        
        # 检查关键文件是否存在
        required_files = [
            "model/model.pt",
            "install/install.sh",
            "start_terminal.sh"
        ]
        
        for file in required_files:
            file_path = os.path.join(target_path, file)
            if os.path.exists(file_path):
                print(f"✓ 找到文件: {file}")
            else:
                print(f"✗ 缺少文件: {file}")
                return False
        
        print("终端设备部署测试通过!")
        return True
        
    except Exception as e:
        print(f"测试过程中发生错误: {e}")
        return False
    
    finally:
        # 清理临时目录
        if os.path.exists(target_path):
            print(f"清理临时目录: {target_path}")
            shutil.rmtree(target_path)

if __name__ == "__main__":
    success = test_terminal_deployment()
    sys.exit(0 if success else 1)