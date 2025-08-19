"""
全球脑大模型配置文件
"""

import os

# 区块链网络配置
BITTENSOR_API_KEY = os.environ.get("BITTENSOR_API_KEY", "your_api_key_here")
BITTENSOR_NETWORK = "finney"  # 主网
# BITTENSOR_NETWORK = "test"   # 测试网

# 矩阵神经网络配置
MATRIX_NN_CONFIG = {
    "input_size": 784,
    "hidden_sizes": [256, 128],
    "output_size": 10,
    "activation": "relu",
    "dropout": 0.1
}

# 区块链矩阵神经网络配置
BLOCKCHAIN_MATRIX_NN_CONFIG = {
    "input_size": 784,
    "hidden_sizes": [512, 256, 128],
    "output_size": 10,
    "blockchain_network": "finney",
    "sync_interval": 300  # 同步间隔（秒）
}

# 知识库配置
KNOWLEDGE_BASE_CONFIG = {
    "sync_interval": 300,  # 同步间隔（秒）
    "encryption_key": os.environ.get("ENCRYPTION_KEY", "default_key_32_bytes_long!!"),
    "storage_path": "./knowledge_base/data"
}

# 元学习平台配置
META_LEARNING_CONFIG = {
    "platform_url": "http://meta-learning-platform.global-brain.ai",
    "api_key": os.environ.get("META_LEARNING_API_KEY", "your_meta_learning_api_key"),
    "sync_interval": 600  # 同步间隔（秒）
}

# 部署配置
DEPLOYMENT_CONFIG = {
    "model_repo_url": "http://models.global-brain.ai",
    "install_path": "./install",
    "temp_path": "./temp"
}

# 自我复制配置
REPLICATION_CONFIG = {
    "discovery_port": 8888,
    "discovery_timeout": 5,  # 节点发现超时时间（秒）
    "network_range": "192.168.1"  # 网络扫描范围
}

# 自我拓展配置
EXPANSION_CONFIG = {
    "assessment_interval": 3600,  # 能力评估间隔（秒）
    "optimization_threshold": 0.8  # 优化阈值
}

# 日志配置
LOGGING_CONFIG = {
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "file": "./logs/global_brain.log",
    "max_bytes": 10485760,  # 10MB
    "backup_count": 5
}

# API接口配置
API_INTERFACE_CONFIG = {
    "interface_id": "760738c40dea265a1b636ada47c741017a52c15d",
    "description": "全球脑大模型智能合约执行接口",
    "functions": [
        "data_analysis",
        "anomaly_detection",
        "predict_model",
        "automated_decision",
        "security_audit",
        "data_privacy_protection"
    ],
    "matrix_input_size": 784,
    "matrix_hidden_sizes": [256, 128],
    "matrix_output_size": 10
}