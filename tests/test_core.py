"""
核心组件测试
"""

import sys
import os
import unittest
import torch
import numpy as np
import time

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from core.blockchain_network import BlockchainNetwork
from core.matrix_nn import MatrixNeuralNetwork
from knowledge_base.merkle_tree import MerkleTree


class TestCoreComponents(unittest.TestCase):
    def test_matrix_nn_creation(self):
        """
        测试矩阵神经网络创建
        """
        # 创建一个简单的矩阵神经网络
        model = MatrixNeuralNetwork(input_size=10, hidden_sizes=[20, 15], output_size=5)
        
        # 检查网络结构
        self.assertIsInstance(model, MatrixNeuralNetwork)
        
        # 测试前向传播
        input_data = torch.randn(1, 10)
        output = model(input_data)
        self.assertEqual(output.shape, (1, 5))
        
    def test_matrix_multiplication(self):
        """
        测试矩阵乘法运算
        """
        model = MatrixNeuralNetwork(input_size=10, hidden_sizes=[20, 15], output_size=5)
        
        # 创建两个矩阵
        A = torch.randn(3, 4)
        B = torch.randn(4, 2)
        
        # 执行矩阵乘法
        result = model.matrix_multiply(A, B)
        
        # 检查结果形状
        self.assertEqual(result.shape, (3, 2))
        
        # 验证计算结果
        expected = torch.mm(A, B)
        self.assertTrue(torch.allclose(result, expected))
        
    def test_blockchain_network_init(self):
        """
        测试区块链网络初始化
        """
        # 创建区块链网络实例
        network = BlockchainNetwork(api_key="test_key")
        
        # 检查初始化
        self.assertIsInstance(network, BlockchainNetwork)
        self.assertEqual(network.api_key, "test_key")
        
    def test_smart_contract_creation(self):
        """
        测试智能合约创建
        """
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'contracts'))
        from contracts.smart_contract import SmartContract
        
        # 创建智能合约
        contract = SmartContract(owner="test_owner")
        
        # 检查初始化
        self.assertIsInstance(contract, SmartContract)
        self.assertEqual(contract.owner, "test_owner")
        self.assertIsNotNone(contract.contract_id)
        
    def test_knowledge_sync(self):
        """
        测试知识库同步机制
        """
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'knowledge_base'))
        from knowledge_base.sync_mechanism import KnowledgeSync
        
        # 创建知识库同步对象
        sync1 = KnowledgeSync()
        sync2 = KnowledgeSync()
        
        # 添加知识
        sync1.add_knowledge("key1", {"data": "value1"})
        sync2.add_knowledge("key2", {"data": "value2"})
        
        # 同步知识库
        sync1.sync_with_node(sync2)
        sync2.sync_with_node(sync1)  # 双向同步确保一致性
        
        # 检查同步结果
        self.assertIn("key2", sync1.knowledge_base)
        self.assertIn("key1", sync2.knowledge_base)
        
        # 验证Merkle树根一致性
        self.assertEqual(sync1.get_merkle_root(), sync2.get_merkle_root())
        
    def test_meta_learning_platform(self):
        """
        测试元学习平台
        """
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'meta_learning'))
        from meta_learning.platform import MetaLearningPlatform
        
        # 创建元学习平台
        platform = MetaLearningPlatform()
        
        # 添加元知识
        platform.add_meta_knowledge("test_key", {"data": "test_value"}, "owner1")
        
        # 获取元知识
        result = platform.get_meta_knowledge("test_key", "owner1")
        self.assertEqual(result["data"], "test_value")
        
        # 验证隐私保护功能
        protected_data = platform._protect_data_privacy({"data": "test_value"}, 'confidential')
        self.assertIn('type', protected_data)
        self.assertIn('size', protected_data)
        
    def test_autonomous_deployment(self):
        """
        测试自主部署机制
        """
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'deployment'))
        from deployment.autonomous_deployment import AutonomousDeployment
        
        # 创建自主部署对象
        deployment = AutonomousDeployment(model_repo_url="http://test.repo/model")
        
        # 获取系统信息
        sys_info = deployment.get_system_info()
        self.assertIn("os", sys_info)
        self.assertIn("python_version", sys_info)
        
        # 验证版本管理
        # 注意：这里假设AutonomousDeployment类有get_installed_versions方法
        # versions = deployment.get_installed_versions()
        # self.assertTrue(len(versions) > 0)
        
    def test_self_replication(self):
        """
        测试自我复制机制
        """
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'deployment'))
        from deployment.self_replication import SelfReplication
        
        # 创建自我复制对象
        replication = SelfReplication(model_path="./test_model.pt")
        
        # 计算模型哈希
        model_hash = replication.calculate_model_hash()
        # 对于不存在的文件，应该返回None
        self.assertIsNone(model_hash)
        
        # 验证网络拓扑发现
        # 注意：这里假设SelfReplication类有get_network_topology方法
        # topology = replication.get_network_topology()
        # self.assertIn('discovered_nodes', topology)
        # self.assertIn('total_nodes', topology)
        
    def test_self_expansion(self):
        """
        测试自我拓展机制
        """
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'deployment'))
        from deployment.self_expansion import SelfExpansion
        
        # 创建自我拓展对象
        expansion = SelfExpansion(model_path="./test_model.pt")
        
        # 评估能力
        expansion.assess_capabilities()
        
        # 获取能力评估
        capabilities = expansion.get_capabilities()
        self.assertIn("compute", capabilities)
        self.assertIn("memory", capabilities)
        self.assertIn("storage", capabilities)
        self.assertIn("network", capabilities)

    def test_merkle_tree(self):
        """测试Merkle树实现"""
        # 创建测试数据
        data = ["data1", "data2", "data3", "data4"]
        
        # 构建Merkle树
        tree = MerkleTree(data)
        
        # 验证根哈希存在
        root_hash = tree.get_root_hash()
        self.assertIsNotNone(root_hash)
        
        # 验证包含证明（简化测试）
        proof = tree.get_inclusion_proof("data1")
        self.assertIsInstance(proof, list)
        
    def test_conflict_resolution(self):
        """测试冲突解决机制"""
        # 创建两个知识同步对象
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'knowledge_base'))
        from knowledge_base.sync_mechanism import KnowledgeSync
        
        sync1 = KnowledgeSync()
        sync2 = KnowledgeSync()
        
        # 添加相同键但不同值的知识
        sync1.add_knowledge("conflict_key", "value1")
        sync2.add_knowledge("conflict_key", "value2")
        
        # 解决冲突
        conflicts = sync1.resolve_conflicts(sync2)
        self.assertIn("conflict_key", conflicts)
        
        # 验证能力预测
        # 注意：这里假设SelfExpansion类有predict_capabilities方法
        # predicted = expansion.predict_capabilities(3600)
        # self.assertIn('compute', predicted)
        # self.assertIn('memory', predicted)


if __name__ == "__main__":
    unittest.main()