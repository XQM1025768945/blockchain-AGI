"""
测试所有模块的日志记录功能
"""

import sys
import os

# 添加项目根目录到sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 导入统一日志配置
import logging_config

# 导入所有模块
from deployment.self_replication import SelfReplication
from deployment.global_brain_deployment import GlobalBrainDeployment
from deployment.autonomous_deployment import AutonomousDeployment
from deployment.self_expansion import SelfExpansion

def test_logging():
    """
    测试所有模块的日志记录功能
    """
    print("开始测试日志记录功能...")
    
    # 设置日志配置
    logging_config.setup_logging()
    
    # 测试self_replication模块日志
    self_replication_logger = logging_config.get_logger('self_replication')
    self_replication_logger.info("Self-replication模块日志测试")
    
    # 测试global_brain_deployment模块日志
    global_brain_logger = logging_config.get_logger('global_brain_deployment')
    global_brain_logger.info("Global brain deployment模块日志测试")
    
    # 测试autonomous_deployment模块日志
    autonomous_logger = logging_config.get_logger('autonomous_deployment')
    autonomous_logger.info("Autonomous deployment模块日志测试")
    
    # 测试self_expansion模块日志
    self_expansion_logger = logging_config.get_logger('self_expansion')
    self_expansion_logger.info("Self expansion模块日志测试")
    
    print("日志记录功能测试完成，请查看agi_deployment.log文件")

if __name__ == "__main__":
    test_logging()