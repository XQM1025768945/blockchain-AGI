"""
检查全球脑大模型部署状态的脚本

展示如何获取已部署的终端数量
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from deployment.global_brain_deployment import GlobalBrainDeployment


def main():
    print("=== 全球脑大模型部署状态检查 ===")
    
    # 初始化全球部署模块
    deployment = GlobalBrainDeployment(
        model_repo_url="http://global-brain.repo/models",
        model_path="./model/model.pt"
    )
    
    # 获取部署状态
    print("正在获取部署状态...")
    status = deployment.get_deployment_status()
    
    # 显示部署状态
    print("\n全球部署状态:")
    print(f"- AI脑是否已激活: {status['is_active']}")
    print(f"- 已部署节点数: {status['nodes_deployed']}")
    
    # 显示详细的部署日志
    print("\n部署日志:")
    for log_entry in status['deployment_log']:
        print(f"- {log_entry['timestamp']}: {log_entry['event']} - {log_entry['status']}")
        if 'nodes_deployed' in log_entry:
            print(f"  部署节点数: {log_entry['nodes_deployed']}")
        if 'expansion_plan' in log_entry:
            print(f"  拓展计划: {log_entry['expansion_plan']}")


if __name__ == "__main__":
    main()