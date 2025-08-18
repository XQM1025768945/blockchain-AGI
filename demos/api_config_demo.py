"""
API接口配置演示

演示如何使用配置文件中的API接口配置
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import API_INTERFACE_CONFIG


def main():
    """
    主函数
    """
    print("API接口配置演示")
    
    # 打印API接口配置
    print(f"接口ID: {API_INTERFACE_CONFIG['interface_id']}")
    print(f"接口描述: {API_INTERFACE_CONFIG['description']}")
    print("接口功能:")
    for i, function in enumerate(API_INTERFACE_CONFIG['functions'], 1):
        print(f"  {i}. {function}")
    
    print("\nAPI接口配置演示完成")


if __name__ == "__main__":
    main()