"""
区块链矩阵神经网络演示脚本

展示如何使用区块链矩阵神经网络模型实现去中心化的类脑AI
"""

import sys
import os
import torch
from torch.utils.data import DataLoader, TensorDataset

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.blockchain_matrix_nn import BlockchainMatrixNeuralNetwork
from config import BLOCKCHAIN_MATRIX_NN_CONFIG, BITTENSOR_API_KEY


def create_sample_data():
    """
    创建示例数据
    
    Returns:
        DataLoader: 数据加载器
    """
    # 创建示例数据
    X = torch.randn(1000, BLOCKCHAIN_MATRIX_NN_CONFIG["input_size"])
    y = torch.randn(1000, BLOCKCHAIN_MATRIX_NN_CONFIG["output_size"])
    
    # 创建数据集和数据加载器
    dataset = TensorDataset(X, y)
    data_loader = DataLoader(dataset, batch_size=32, shuffle=True)
    
    return data_loader


def main():
    """
    主函数
    """
    print("初始化区块链矩阵神经网络...")
    
    # 创建区块链矩阵神经网络
    model = BlockchainMatrixNeuralNetwork(
        input_size=BLOCKCHAIN_MATRIX_NN_CONFIG["input_size"],
        hidden_sizes=BLOCKCHAIN_MATRIX_NN_CONFIG["hidden_sizes"],
        output_size=BLOCKCHAIN_MATRIX_NN_CONFIG["output_size"],
        api_key=BITTENSOR_API_KEY
    )
    
    # 创建示例数据
    print("创建示例数据...")
    data_loader = create_sample_data()
    
    # 训练模型
    print("开始训练模型...")
    model.train_model(data_loader, epochs=5, learning_rate=0.001)
    
    # 计算模型哈希
    print("计算模型哈希...")
    model_hash = model.calculate_model_hash()
    print(f"模型哈希: {model_hash}")
    
    # 保存模型
    print("保存模型...")
    model.save_model("./blockchain_matrix_model.pt")
    print("模型已保存到 ./blockchain_matrix_model.pt")
    
    print("区块链矩阵神经网络演示完成")


if __name__ == "__main__":
    main()