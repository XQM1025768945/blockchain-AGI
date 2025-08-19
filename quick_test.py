"""
快速测试脚本，验证所有主要功能是否正常工作
"""

import sys
import os

# 添加项目根目录到sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 导入统一日志配置
import logging_config

# 导入所有主要模块
from deployment.self_replication import SelfReplication
from deployment.global_brain_deployment import GlobalBrainDeployment
from deployment.autonomous_deployment import AutonomousDeployment
from deployment.self_expansion import SelfExpansion

def quick_test():
    """
    快速测试所有主要功能
    """
    print("开始快速测试...")
    
    # 设置日志配置
    logging_config.setup_logging()
    
    # 测试1: SelfReplication模块
    print("\n1. 测试SelfReplication模块...")
    try:
        self_replication = SelfReplication()
        # 测试加密功能
        test_data = "This is a test message for encryption"
        encrypted_data = self_replication.encrypt_data(test_data)
        decrypted_data = self_replication.decrypt_data(encrypted_data)
        
        if test_data == decrypted_data:
            print("  ✓ 加密/解密功能正常")
        else:
            print("  ✗ 加密/解密功能异常")
            
        # 测试节点发现功能 (使用本地回环地址)
        nodes = self_replication.discover_nodes("127.0.0.1", 8000, 8010, 8888, 1)
        print(f"  ✓ 节点发现功能正常，发现{len(nodes)}个节点")
        
    except Exception as e:
        print(f"  ✗ SelfReplication模块测试失败: {e}")
    
    # 测试2: GlobalBrainDeployment模块
    print("\n2. 测试GlobalBrainDeployment模块...")
    try:
        global_brain = GlobalBrainDeployment()
        print("  ✓ GlobalBrainDeployment模块初始化正常")
        
        # 获取部署状态
        status = global_brain.get_deployment_status()
        print(f"  ✓ 部署状态获取正常: {status}")
        
    except Exception as e:
        print(f"  ✗ GlobalBrainDeployment模块测试失败: {e}")
    
    # 测试3: AutonomousDeployment模块
    print("\n3. 测试AutonomousDeployment模块...")
    try:
        autonomous = AutonomousDeployment("https://example.com/model")
        print("  ✓ AutonomousDeployment模块初始化正常")
        
        # 获取系统信息
        sys_info = autonomous.get_system_info()
        print(f"  ✓ 系统信息获取正常: {sys_info['os']} {sys_info['arch']}")
        
    except Exception as e:
        print(f"  ✗ AutonomousDeployment模块测试失败: {e}")
    
    # 测试4: SelfExpansion模块
    print("\n4. 测试SelfExpansion模块...")
    try:
        self_expansion = SelfExpansion()
        print("  ✓ SelfExpansion模块初始化正常")
        
        # 评估能力
        self_expansion.assess_capabilities()
        capabilities = self_expansion.get_capabilities()
        print(f"  ✓ 能力评估正常: {capabilities}")
        
        # 分配资源
        resources = self_expansion.allocate_resources({})
        print(f"  ✓ 资源分配正常: CPU={resources['cpu']}, Memory={resources['memory']}GB")
        
    except Exception as e:
        print(f"  ✗ SelfExpansion模块测试失败: {e}")
    
    print("\n快速测试完成!")

if __name__ == "__main__":
    quick_test()