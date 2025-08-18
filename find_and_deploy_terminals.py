"""
寻找并部署到终端设备的演示脚本
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from deployment.global_brain_deployment import GlobalBrainDeployment


def main():
    print("开始寻找可以部署的终端设备...")
    
    # 初始化全球AI脑部署机制
    deployment = GlobalBrainDeployment(
        model_repo_url="http://global-brain.repo/models",
        model_path="./model/model.pt"
    )
    
    # 在全球范围内部署AI脑（这将自动发现网络中的节点并部署）
    print("\n1. 开始全球部署...")
    success = deployment.deploy_globally(network_range="192.168.1", port=8888)
    
    if success:
        print("\n全球部署成功完成！")
        print(f"已发现并部署到 {len(deployment.replication.nodes)} 个终端设备:")
        for i, node in enumerate(deployment.replication.nodes, 1):
            print(f"  {i}. {node}:8888")
    else:
        print("\n全球部署失败。")
        
    # 获取部署状态
    status = deployment.get_deployment_status()
    print(f"\n部署状态: {status}")
    
    # 激活全球AI脑
    print("\n2. 激活全球AI脑...")
    activation_success = deployment.activate_globally()
    
    if activation_success:
        print("\n全球AI脑激活成功！")
    else:
        print("\n全球AI脑激活失败。")
        
    # 能力拓展
    print("\n3. 开始能力拓展...")
    expansion_plan = {
        "compute": 15.0,   # 提升15%计算能力
        "memory": 25.0,   # 提升25%内存能力
        "storage": 10.0,  # 提升10%存储能力
        "network": 20.0   # 提升20%网络能力
    }
    
    expansion_success = deployment.expand_globally(expansion_plan)
    
    if expansion_success:
        print("\n能力拓展成功完成！")
    else:
        print("\n能力拓展失败。")


if __name__ == "__main__":
    main()