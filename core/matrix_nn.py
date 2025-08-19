"""
矩阵神经网络模块

基于PyTorch实现矩阵运算神经网络
"""

import sys
import os

# 添加项目根目录到sys.path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

import torch
import torch.nn as nn
import numpy as np

# 导入统一日志配置
import logging_config

# 获取日志记录器
logger = logging_config.get_logger('matrix_nn')


class MatrixNeuralNetwork(nn.Module):
    def __init__(self, input_size, hidden_sizes, output_size):
        """
        初始化矩阵神经网络
        
        Args:
            input_size (int): 输入层大小
            hidden_sizes (list): 隐藏层大小列表
            output_size (int): 输出层大小
        """
        super(MatrixNeuralNetwork, self).__init__()
        
        # 创建网络层
        layers = []
        prev_size = input_size
        
        # 添加隐藏层
        for hidden_size in hidden_sizes:
            layers.append(nn.Linear(prev_size, hidden_size))
            layers.append(nn.ReLU())
            prev_size = hidden_size
            
        # 添加输出层
        layers.append(nn.Linear(prev_size, output_size))
        
        # 创建网络
        self.network = nn.Sequential(*layers)
        
    def forward(self, x):
        """
        前向传播
        
        Args:
            x (torch.Tensor): 输入数据
            
        Returns:
            torch.Tensor: 输出结果
        """
        return self.network(x)
        
    def matrix_multiply(self, A, B):
        """
        矩阵乘法运算
        
        Args:
            A (torch.Tensor): 矩阵A
            B (torch.Tensor): 矩阵B
            
        Returns:
            torch.Tensor: 运算结果
        """
        return torch.mm(A, B)
        
    def train_model(self, data_loader, epochs, learning_rate=0.001):
        """
        训练模型
        
        Args:
            data_loader (DataLoader): 数据加载器
            epochs (int): 训练轮数
            learning_rate (float): 学习率
        """
        criterion = nn.MSELoss()
        optimizer = torch.optim.Adam(self.parameters(), lr=learning_rate)
        
        for epoch in range(epochs):
            for batch_idx, (data, target) in enumerate(data_loader):
                optimizer.zero_grad()
                output = self.forward(data)
                loss = criterion(output, target)
                loss.backward()
                optimizer.step()
                
                if batch_idx % 100 == 0:
                    logger.info(f'Epoch {epoch}, Batch {batch_idx}, Loss: {loss.item()}')
                    
    def save_model(self, path):
        """
        保存模型
        
        Args:
            path (str): 保存路径
        """
        torch.save(self.state_dict(), path)
        
    def load_model(self, path):
        """
        加载模型
        
        Args:
            path (str): 模型路径
        """
        self.load_state_dict(torch.load(path))