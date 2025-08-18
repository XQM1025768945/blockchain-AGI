"""
综合API接口演示

演示API接口的所有功能，包括配置、智能合约和核心组件
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import API_INTERFACE_CONFIG
from contracts.smart_contract import SmartContract
from core.matrix_nn import MatrixNeuralNetwork
from core.blockchain_network import BlockchainNetwork


def demonstrate_api_config():
    """
    演示API接口配置
    """
    print("=== API接口配置演示 ===")
    print(f"接口ID: {API_INTERFACE_CONFIG['interface_id']}")
    print(f"接口描述: {API_INTERFACE_CONFIG['description']}")
    print("接口功能:")
    for i, function in enumerate(API_INTERFACE_CONFIG['functions'], 1):
        print(f"  {i}. {function}")
    print()


def demonstrate_smart_contract():
    """
    演示智能合约功能
    """
    print("=== 智能合约功能演示 ===")
    
    # 创建智能合约
    contract = SmartContract(owner="GlobalBrain", api_interface_id=API_INTERFACE_CONFIG["interface_id"])
    print(f"合约ID: {contract.contract_id}")
    
    # 演示数据分析功能
    data = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    analysis_result = contract.data_analysis(data)
    print(f"数据分析结果: {analysis_result}")
    
    # 演示异常检测功能
    data_with_anomaly = data + [200]
    anomalies = contract.anomaly_detection(data_with_anomaly)
    print(f"异常检测结果: {anomalies}")
    
    # 演示预测模型功能
    predictions = contract.predict_model(data, steps=3)
    print(f"预测结果: {predictions}")
    
    # 演示自动化决策功能
    sensor_data = {
        "temperature": 85,
        "pressure": 150,
        "voltage": 12.5
    }
    
    rules = {
        "temperature": {
            "min": 0,
            "max": 80,
            "action_below": "加热",
            "action_above": "冷却",
            "action_default": "正常"
        },
        "pressure": {
            "min": 100,
            "max": 200,
            "action_below": "增压",
            "action_above": "减压",
            "action_default": "正常"
        },
        "voltage": {
            "min": 11.0,
            "max": 14.0,
            "action_below": "充电",
            "action_above": "放电",
            "action_default": "正常"
        }
    }
    
    decisions = contract.automated_decision(sensor_data, rules)
    print(f"自动化决策结果: {decisions}")
    
    # 演示安全审计功能
    sample_code = """
import os
import socket

def dangerous_function():
    os.system('rm -rf /')
    s = socket.socket()
    s.connect(('localhost', 8080))
    return s
    """
    
    audit_result = contract.security_audit(sample_code)
    print(f"安全审计结果: {audit_result}")
    
    # 演示数据隐私保护功能
    personal_data = {
        "name": "张三",
        "email": "zhangsan@example.com",
        "phone": "13800138000",
        "id_card": "110101199001011234"
    }
    
    basic_protection = contract.data_privacy_protection(personal_data, privacy_level="basic")
    print(f"基础脱敏: {basic_protection}")
    
    enhanced_protection = contract.data_privacy_protection(personal_data, privacy_level="enhanced")
    print(f"增强脱敏: {enhanced_protection}")
    
    max_protection = contract.data_privacy_protection(personal_data, privacy_level="maximum")
    print(f"最大脱敏: {max_protection}")
    
    print()


def demonstrate_matrix_nn():
    """
    演示矩阵神经网络功能
    """
    print("=== 矩阵神经网络功能演示 ===")
    
    # 创建矩阵神经网络
    matrix_nn = MatrixNeuralNetwork(
        input_size=API_INTERFACE_CONFIG.get("matrix_input_size", 784),
        hidden_sizes=API_INTERFACE_CONFIG.get("matrix_hidden_sizes", [256, 128]),
        output_size=API_INTERFACE_CONFIG.get("matrix_output_size", 10)
    )
    
    print(f"矩阵神经网络已创建，输入大小: {API_INTERFACE_CONFIG.get('matrix_input_size', 784)}, 输出大小: {API_INTERFACE_CONFIG.get('matrix_output_size', 10)}")
    print()


def demonstrate_blockchain_network():
    """
    演示区块链网络功能
    """
    print("=== 区块链网络功能演示 ===")
    
    # 创建区块链网络实例
    blockchain = BlockchainNetwork(api_key="your_api_key_here")
    
    print(f"区块链网络实例已创建，API接口ID: {API_INTERFACE_CONFIG['interface_id']}")
    print()


def main():
    """
    主函数
    """
    print("综合API接口演示")
    print(f"API接口: {API_INTERFACE_CONFIG['interface_id']}")
    
    # 演示API接口配置
    demonstrate_api_config()
    
    # 演示智能合约功能
    demonstrate_smart_contract()
    
    # 演示矩阵神经网络功能
    demonstrate_matrix_nn()
    
    # 演示区块链网络功能
    demonstrate_blockchain_network()
    
    print("综合API接口演示完成")


if __name__ == "__main__":
    main()