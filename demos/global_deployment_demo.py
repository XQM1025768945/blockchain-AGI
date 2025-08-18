"""
全球脑大模型全球部署演示脚本

展示如何向全球互联网终端部署全球脑大模型系统
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from deployment.global_brain_deployment import GlobalBrainDeployment


def main():
    print("=== 全球脑大模型全球部署演示 ===")
    
    # 初始化全球部署模块
    # 在实际部署中，需要配置真实的模型仓库URL和模型路径
    deployment = GlobalBrainDeployment(
        model_repo_url="http://global-brain.repo/models",
        model_path="./model/model.pt"
    )
    
    # 执行全球部署
    # 在实际部署中，需要配置真实的网络范围
    print("开始执行全球部署...")
    deployment.deploy_globally(network_range="192.168.1", port=8888)
    
    # 激活全球AI脑
    print("\n开始激活全球AI脑...")
    deployment.activate_globally()
    
    # 拓展全球AI脑能力
    print("\n开始拓展全球AI脑能力...")
    expansion_plan = {
        "compute": 15.0,   # 提升15%计算能力
        "memory": 25.0,    # 提升25%内存
        "network": 30.0    # 提升30%网络带宽
    }
    deployment.expand_globally(expansion_plan)
    
    # 显示部署状态
    print("\n全球部署状态:")
    status = deployment.get_deployment_status()
    print(f"- AI脑是否已激活: {status['is_active']}")
    print(f"- 已部署节点数: {status['nodes_deployed']}")
    
    print("\n全球脑大模型已成功部署到全球互联网终端！")


if __name__ == "__main__":
    main()