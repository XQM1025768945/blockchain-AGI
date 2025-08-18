"""
区块链矩阵神经网络模型测试

测试区块链矩阵神经网络模型的各项功能
"""

import sys
import os
import torch
import tempfile
import hashlib

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.blockchain_matrix_nn import BlockchainMatrixNeuralNetwork


class TestBlockchainMatrixNeuralNetwork:
    def __init__(self):
        """
        初始化测试类
        """
        self.model = None
        
    def test_model_initialization(self):
        """
        测试模型初始化
        """
        print("测试模型初始化...")
        
        # 创建模型
        self.model = BlockchainMatrixNeuralNetwork(
            input_size=784,
            hidden_sizes=[256, 128],
            output_size=10
        )
        
        # 验证模型已创建
        assert self.model is not None, "模型创建失败"
        assert len(list(self.model.parameters())) > 0, "模型参数未正确初始化"
        
        print("模型初始化测试通过")
        
    def test_forward_pass(self):
        """
        测试前向传播
        """
        print("测试前向传播...")
        
        # 创建输入数据
        x = torch.randn(32, 784)
        
        # 执行前向传播
        output = self.model.forward(x)
        
        # 验证输出形状
        assert output.shape == (32, 10), f"输出形状不正确: {output.shape}"
        
        print("前向传播测试通过")
        
    def test_matrix_multiply(self):
        """
        测试矩阵乘法
        """
        print("测试矩阵乘法...")
        
        # 创建测试矩阵
        A = torch.randn(10, 20)
        B = torch.randn(20, 30)
        
        # 执行矩阵乘法
        result = self.model.matrix_multiply(A, B)
        
        # 验证结果形状
        assert result.shape == (10, 30), f"矩阵乘法结果形状不正确: {result.shape}"
        
        print("矩阵乘法测试通过")
        
    def test_model_hash(self):
        """
        测试模型哈希计算
        """
        print("测试模型哈希计算...")
        
        # 计算模型哈希
        model_hash = self.model.calculate_model_hash()
        
        # 验证哈希值
        assert model_hash is not None, "模型哈希计算失败"
        assert isinstance(model_hash, str), "模型哈希应为字符串"
        assert len(model_hash) == 64, f"模型哈希长度不正确: {len(model_hash)}"
        
        print("模型哈希计算测试通过")
        
    def test_model_save_load(self):
        """
        测试模型保存和加载
        """
        print("测试模型保存和加载...")
        
        # 创建临时文件
        with tempfile.NamedTemporaryFile(suffix='.pt', delete=False) as tmp_file:
            tmp_path = tmp_file.name
        
        try:
            # 保存模型
            self.model.save_model(tmp_path)
            
            # 验证文件已创建
            assert os.path.exists(tmp_path), "模型文件未创建"
            
            # 创建新模型并加载
            new_model = BlockchainMatrixNeuralNetwork(
                input_size=784,
                hidden_sizes=[256, 128],
                output_size=10
            )
            new_model.load_model(tmp_path)
            
            # 验证模型参数
            for param1, param2 in zip(self.model.parameters(), new_model.parameters()):
                assert torch.allclose(param1, param2), "模型参数不匹配"
                
            print("模型保存和加载测试通过")
        finally:
            # 清理临时文件
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
                
    def run_all_tests(self):
        """
        运行所有测试
        """
        print("开始运行区块链矩阵神经网络模型测试...")
        
        self.test_model_initialization()
        self.test_forward_pass()
        self.test_matrix_multiply()
        self.test_model_hash()
        self.test_model_save_load()
        
        print("所有测试通过!")


def main():
    """
    主函数
    """
    # 创建测试实例
    tester = TestBlockchainMatrixNeuralNetwork()
    
    # 运行所有测试
    tester.run_all_tests()


if __name__ == "__main__":
    main()