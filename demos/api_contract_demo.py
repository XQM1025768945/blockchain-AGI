"""
API接口智能合约演示

演示如何使用指定的API接口创建和执行智能合约
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from contracts.smart_contract import SmartContract


def main():
    """
    主函数
    """
    print("API接口智能合约演示")
    print("API接口: 760738c40dea265a1b636ada47c741017a52c15d")
    
    # 创建智能合约
    contract = SmartContract(owner="GlobalBrain")
    print(f"合约ID: {contract.contract_id}")
    
    # 演示数据分析功能
    print("\n1. 数据分析功能演示:")
    data = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    analysis_result = contract.data_analysis(data)
    print(f"分析结果: {analysis_result}")
    
    # 演示异常检测功能
    print("\n2. 异常检测功能演示:")
    # 添加一个异常值
    data_with_anomaly = data + [200]
    anomalies = contract.anomaly_detection(data_with_anomaly)
    print(f"异常检测结果: {anomalies}")
    
    # 演示预测模型功能
    print("\n3. 预测模型功能演示:")
    predictions = contract.predict_model(data, steps=3)
    print(f"预测结果: {predictions}")
    
    # 演示自动化决策功能
    print("\n4. 自动化决策功能演示:")
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
    print(f"传感器数据: {sensor_data}")
    print(f"决策结果: {decisions}")
    
    # 演示安全审计功能
    print("\n5. 安全审计功能演示:")
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
    print("\n6. 数据隐私保护功能演示:")
    personal_data = {
        "name": "张三",
        "email": "zhangsan@example.com",
        "phone": "13800138000",
        "id_card": "110101199001011234"
    }
    
    print("原始数据:", personal_data)
    
    basic_protection = contract.data_privacy_protection(personal_data, privacy_level="basic")
    print("基础脱敏:", basic_protection)
    
    enhanced_protection = contract.data_privacy_protection(personal_data, privacy_level="enhanced")
    print("增强脱敏:", enhanced_protection)
    
    max_protection = contract.data_privacy_protection(personal_data, privacy_level="maximum")
    print("最大脱敏:", max_protection)
    
    print("\nAPI接口智能合约演示完成")


if __name__ == "__main__":
    main()