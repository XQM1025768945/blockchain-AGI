"""并行运行终端节点和测试脚本

这个脚本将并行启动增强版终端节点和通信测试。
"""

import subprocess
import sys
import os
import time
import threading


def run_terminal_node():
    """运行终端节点"""
    try:
        print("启动增强版终端节点...")
        # 使用subprocess运行终端节点脚本
        script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "enhanced_terminal_node.py")
        process = subprocess.Popen(
            [sys.executable, script_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # 等待几秒钟让节点启动
        time.sleep(3)
        
        # 检查进程是否仍在运行
        if process.poll() is None:
            print("终端节点已启动并正在运行")
            return process
        else:
            stdout, stderr = process.communicate()
            print(f"终端节点启动失败: {stderr}")
            return None
    except Exception as e:
        print(f"启动终端节点时出错: {e}")
        return None


def run_communication_test():
    """运行通信测试"""
    try:
        print("运行通信测试...")
        # 使用subprocess运行通信测试脚本
        script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_node_communication.py")
        result = subprocess.run(
            [sys.executable, script_path],
            capture_output=True,
            text=True
        )
        
        print("通信测试输出:")
        print(result.stdout)
        
        if result.stderr:
            print("通信测试错误:")
            print(result.stderr)
        
        return result.returncode == 0
    except Exception as e:
        print(f"运行通信测试时出错: {e}")
        return False


def main():
    print("=== 并行运行终端节点和测试 ===")
    
    # 启动终端节点
    node_process = run_terminal_node()
    
    if node_process:
        # 等待几秒钟确保节点完全启动
        time.sleep(5)
        
        # 运行通信测试
        test_success = run_communication_test()
        
        # 终止终端节点
        print("终止终端节点...")
        node_process.terminate()
        try:
            node_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            node_process.kill()
        
        if test_success:
            print("\n通信测试成功完成!")
        else:
            print("\n通信测试失败!")
    else:
        print("无法启动终端节点，测试无法进行")
    
    print("=== 运行完成 ===")


if __name__ == "__main__":
    main()