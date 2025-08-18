# 区块链矩阵神经网络模型

## 简介

区块链矩阵神经网络模型是一个结合了区块链技术和矩阵神经网络的去中心化AI模型。它利用区块链网络实现模型的分布式存储和同步，同时利用矩阵神经网络进行高效的计算。

## 架构

区块链矩阵神经网络模型由两个主要部分组成：

1. **矩阵神经网络**：基于PyTorch实现的深度神经网络，用于执行机器学习任务。
2. **区块链网络接口**：基于Bittensor实现的区块链网络接口，用于与去中心化网络进行交互。

## 功能

- 模型训练：支持本地训练和分布式训练
- 模型哈希计算：计算模型的唯一哈希值，用于验证模型完整性
- 模型保存和加载：支持模型的持久化存储
- 区块链网络连接：连接到Bittensor网络
- 模型分发：将模型分发到区块链网络中的其他节点
- 权重同步：与区块链网络中的其他节点同步模型权重

## 使用方法

### 初始化模型

```python
from core.blockchain_matrix_nn import BlockchainMatrixNeuralNetwork

model = BlockchainMatrixNeuralNetwork(
    input_size=784,
    hidden_sizes=[512, 256, 128],
    output_size=10,
    api_key="your_bittensor_api_key"
)
```

### 训练模型

```python
# 创建数据加载器
from torch.utils.data import DataLoader, TensorDataset

# 假设你已经有了训练数据 X 和标签 y
# dataset = TensorDataset(X, y)
# data_loader = DataLoader(dataset, batch_size=32, shuffle=True)

# 训练模型
model.train_model(data_loader, epochs=10, learning_rate=0.001)
```

### 计算模型哈希

```python
model_hash = model.calculate_model_hash()
print(f"模型哈希: {model_hash}")
```

### 保存模型

```python
model.save_model("./blockchain_matrix_model.pt")
```

### 连接到区块链网络

```python
try:
    model.connect_blockchain()
    print("成功连接到区块链网络")
except Exception as e:
    print(f"连接区块链网络失败: {e}")
```

### 分发模型到区块链网络

```python
try:
    model.distribute_model()
    print("模型分发完成")
except Exception as e:
    print(f"模型分发失败: {e}")
```

### 与区块链网络同步权重

```python
try:
    model.synchronize_weights()
    print("权重同步完成")
except Exception as e:
    print(f"权重同步失败: {e}")
```

## 配置

在 `config.py` 文件中可以配置区块链矩阵神经网络的相关参数：

```python
# 区块链矩阵神经网络配置
BLOCKCHAIN_MATRIX_NN_CONFIG = {
    "input_size": 784,
    "hidden_sizes": [512, 256, 128],
    "output_size": 10,
    "blockchain_network": "finney",
    "sync_interval": 300  # 同步间隔（秒）
}
```

## 运行演示

可以通过运行演示脚本来查看区块链矩阵神经网络的工作流程：

```bash
cd z:\AGI
python demos/blockchain_matrix_demo.py
```

## 运行测试

可以通过运行测试来验证区块链矩阵神经网络的各项功能：

```bash
cd z:\AGI
python -m tests.test_blockchain_matrix_nn
```