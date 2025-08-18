"""全球脑模型激活和通信演示脚本

这个脚本演示如何激活全球AI脑模型并尝试进行通信和对话交流。
"""

import sys
import os

# 添加项目根目录到系统路径
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from deployment.global_brain_deployment import GlobalBrainDeployment


def main():
    print("=== 全球脑模型激活和通信演示 ===")
    
    # 初始化全球脑部署模块
    print("\n1. 初始化全球脑部署模块...")
    brain = GlobalBrainDeployment(
        model_repo_url="http://global-brain.repo/models",
        model_path="./model/model.pt"
    )
    
    # 显示当前部署状态
    print("\n2. 检查当前部署状态...")
    status = brain.get_deployment_status()
    print(f"   AI脑是否激活: {status['is_active']}")
    print(f"   已部署节点数: {status['nodes_deployed']}")
    
    # 激活全球AI脑
    print("\n3. 激活全球AI脑...")
    if brain.activate_globally():
        print("   全球AI脑激活成功!")
    else:
        print("   全球AI脑激活失败!")
        return
    
    # 重新检查部署状态
    print("\n4. 重新检查部署状态...")
    status = brain.get_deployment_status()
    print(f"   AI脑是否激活: {status['is_active']}")
    print(f"   已部署节点数: {status['nodes_deployed']}")
    
    # 模拟通信对话
    print("\n5. 开始通信对话演示...")
    if status['is_active']:
        print("   [AI脑] 你好！我是全球AI脑，已经成功激活。")
        print("   [AI脑] 我可以同时与 {} 个节点进行通信。".format(status['nodes_deployed']))
        
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


if __name__ == "__main__":
    main()