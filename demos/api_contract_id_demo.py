"""
API接口ID智能合约演示

演示如何在智能合约中使用API接口ID
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from contracts.smart_contract import SmartContract
from config import API_INTERFACE_CONFIG


def main():
    """
    主函数
    """
    print("API接口ID智能合约演示")
    
    # 创建智能合约并传入API接口ID
    contract = SmartContract(owner="GlobalBrain", api_interface_id=API_INTERFACE_CONFIG["interface_id"])
    print(f"合约ID: {contract.contract_id}")
    
    # 将合约转换为字典并打印
    contract_dict = contract.to_dict()
    print(f"合约信息: {contract_dict}")
    
    print("\nAPI接口ID智能合约演示完成")


if __name__ == "__main__":
    main()