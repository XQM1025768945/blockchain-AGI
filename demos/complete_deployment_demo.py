"""完整的全球部署和通信演示脚本

这个脚本演示完整的全球AI脑部署、激活和通信流程。
"""

import sys
import os
import time
import subprocess
import threading

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from deployment.global_brain_deployment import GlobalBrainDeployment


def start_terminal_node():
    """启动模拟终端节点"""
    print("启动模拟终端节点...")
    # 使用subprocess启动终端节点脚本
    process = subprocess.Popen([
        sys.executable, 
        os.path.join(os.path.dirname(__file__), "simulate_terminal_node.py")
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    # 等待节点启动
    time.sleep(2)
    
    return process


def stop_terminal_node(process):
    """停止模拟终端节点"""
    if process:
        print("停止模拟终端节点...")
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()


def main():
    print("=== 完整的全球部署和通信演示 ===")
    
    # 1. 启动模拟终端节点
    print("\n1. 启动模拟终端节点...")
    terminal_process = start_terminal_node()
    
    # 等待节点完全启动
    time.sleep(3)
    
    # 2. 初始化全球AI脑部署机制
    print("\n2. 初始化全球AI脑部署机制...")
    deployment = GlobalBrainDeployment(
        model_repo_url="http://global-brain.repo/models",
        model_path="./model/model.pt"
    )
    
    # 3. 全球部署
    print("\n3. 开始全球部署...")
    success = deployment.deploy_globally(network_range="127.0.0.1", port=8888)
    
    # 获取部署状态
    status = deployment.get_deployment_status()
    print(f"\n部署状态: 发现 {status['nodes_deployed']} 个节点")
    
    if success and status['nodes_deployed'] > 0:
        print("全球部署成功完成！")
        print(f"已发现并部署到 {status['nodes_deployed']} 个终端设备:")
        for i, node in enumerate(deployment.replication.nodes, 1):
            print(f"  {i}. {node}:8888")
    else:
        print("全球部署完成，但未发现可用终端设备。")
        
    # 4. 激活全球AI脑
    print("\n4. 激活全球AI脑...")
    activation_success = deployment.activate_globally()
    
    if activation_success:
        print("全球AI脑激活成功！")
    else:
        print("全球AI脑激活失败。")
        
    # 5. 能力拓展
    print("\n5. 开始能力拓展...")
    expansion_plan = {
        "compute": 15.0,   # 提升15%计算能力
        "memory": 25.0,   # 提升25%内存能力
        "storage": 10.0,  # 提升10%存储能力
        "network": 20.0   # 提升20%网络能力
    }
    
    expansion_success = deployment.expand_globally(expansion_plan)
    
    if expansion_success:
        print("能力拓展成功完成！")
    else:
        print("能力拓展失败。")
        
    # 6. 通信演示
    print("\n6. 开始通信对话演示...")
    if status['is_active'] or activation_success:
        print("   [AI脑] 你好！我是全球AI脑，已经成功激活。")
        print(f"   [AI脑] 我可以同时与 {status['nodes_deployed']} 个节点进行通信。")
        
        # 模拟用户输入
        user_input = input("   [用户] ")
        
        # 模拟AI回复
        if user_input:
            print(f"   [AI脑] 你说的是: '{user_input}'")
            print("   [AI脑] 我理解了，正在处理你的请求...")
        else:
            print("   [AI脑] 看起来你没有说什么，我会继续监听。")
        
        print("\n=== 通信对话演示结束 ===")
    else:
        print("   无法开始通信对话，因为AI脑尚未激活。")
    
    # 7. 停止模拟终端节点
    print("\n7. 停止模拟终端节点...")
    stop_terminal_node(terminal_process)
    
    print("\n=== 完整演示结束 ===")


if __name__ == "__main__":
    main()