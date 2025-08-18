"""
全球脑大模型使用示例
"""

import sys
import os

# 添加项目目录到Python路径
sys.path.insert(0, os.path.dirname(__file__))

from core.blockchain_network import BlockchainNetwork
from core.matrix_nn import MatrixNeuralNetwork
from contracts.smart_contract import SmartContract
from knowledge_base.sync_mechanism import KnowledgeSync
from meta_learning.platform import MetaLearningPlatform


def example_blockchain_network():
    """
    区块链网络使用示例
    """
    print("=== 区块链网络使用示例 ===")
    
    # 初始化区块链网络
    blockchain = BlockchainNetwork(api_key="test_key")
    print(f"区块链网络已初始化")
    
    # 连接到网络（在实际使用中需要有效的API密钥）
    # blockchain.connect()
    # print("已连接到区块链网络")
    
    # 获取节点列表（在实际使用中会返回真实节点列表）
    nodes = blockchain.get_nodes()
    print(f"网络节点列表: {nodes}")
    
    print()


def example_matrix_nn():
    """
    矩阵神经网络使用示例
    """
    print("=== 矩阵神经网络使用示例 ===")
    
    # 初始化矩阵神经网络
    matrix_nn = MatrixNeuralNetwork(input_size=10, hidden_sizes=[20, 15], output_size=5)
    print(f"矩阵神经网络已创建，参数数量: {sum(p.numel() for p in matrix_nn.parameters())}")
    
    # 执行矩阵乘法运算
    import torch
    a = torch.randn(3, 10)
    b = torch.randn(10, 5)
    result = matrix_nn.matrix_multiply(a, b)
    print(f"矩阵乘法运算结果形状: {result.shape}")
    
    print()


def example_smart_contract():
    """
    智能合约使用示例
    """
    print("=== 智能合约使用示例 ===")
    
    # 创建智能合约
    contract = SmartContract(owner="example_user")
    print(f"智能合约已创建: {contract.contract_id}")
    
    # 数据分析
    data = [1, 2, 3, 4, 5, 100, 6, 7, 8, 9, 10]
    analysis = contract.data_analysis(data)
    print(f"数据分析结果: {analysis}")
    
    # 异常检测
    anomalies = contract.anomaly_detection(data)
    print(f"异常检测结果: {anomalies}")
    
    # 趋势预测
    prediction = contract.predict_trend(data)
    print(f"趋势预测结果: {prediction}")
    
    # 自动化决策
    decision = contract.make_decision(data)
    print(f"自动化决策结果: {decision}")
    
    print()


def example_knowledge_sync():
    """
    知识库同步机制使用示例
    """
    print("=== 知识库同步机制使用示例 ===")
    
    # 初始化知识库同步机制
    knowledge_sync = KnowledgeSync()
    print("知识库同步机制已初始化")
    
    # 添加知识
    knowledge_sync.add_knowledge("example_key", {
        "title": "示例知识",
        "content": "这是一个示例知识条目",
        "tags": ["example", "test"]
    })
    print("已添加示例知识")
    
    # 获取知识
    knowledge = knowledge_sync.get_knowledge("example_key")
    print(f"获取到的知识: {knowledge}")
    
    # 验证数据完整性
    is_valid = knowledge_sync.verify_integrity()
    print(f"数据完整性验证结果: {is_valid}")
    
    print()


def example_meta_learning():
    """
    元学习云共享平台使用示例
    """
    print("=== 元学习云共享平台使用示例 ===")
    
    # 初始化元学习平台
    meta_learning = MetaLearningPlatform()
    print("元学习云共享平台已初始化")
    
    # 添加元知识
    meta_learning.add_meta_knowledge("example_strategy", {
        "type": "federated_learning",
        "aggregation": "fedavg",
        "compression": True
    }, owner="example_user")
    print("已添加示例元知识")
    
    # 获取元知识
    meta_knowledge = meta_learning.get_meta_knowledge("example_strategy")
    print(f"获取到的元知识: {meta_knowledge}")
    
    # 搜索元知识
    results = meta_learning.search_meta_knowledge("federated")
    print(f"搜索结果: {results}")
    
    print()


def main():
    """
    主函数
    """
    print("全球脑大模型使用示例")
    print("========================")
    
    example_blockchain_network()
    example_matrix_nn()
    example_smart_contract()
    example_knowledge_sync()
    example_meta_learning()
    
    print("所有示例执行完成")


if __name__ == "__main__":
    main()