"""终端节点通信测试脚本

这个脚本用于测试与终端节点的通信功能，包括发送激活信号、能力拓展计划等。
"""

import socket
import json
import time
from cryptography.fernet import Fernet


def send_activation_signal(host="127.0.0.1", port=8888):
    """发送激活信号到终端节点"""
    try:
        # 创建socket连接
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))
        
        # 构造激活信号
        signal = {
            "type": "activation",
            "timestamp": time.time(),
            "message": "激活终端节点"
        }
        
        # 发送信号
        client_socket.sendall(json.dumps(signal).encode())
        
        # 接收响应
        response_data = client_socket.recv(4096)
        response = json.loads(response_data.decode())
        
        print(f"激活信号发送成功: {signal}")
        print(f"节点响应: {response}")
        
        return response
    except Exception as e:
        print(f"发送激活信号时出错: {e}")
        return None
    finally:
        client_socket.close()


def send_expansion_plan(host="127.0.0.1", port=8888):
    """发送能力拓展计划到终端节点"""
    try:
        # 创建socket连接
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))
        
        # 构造能力拓展计划
        plan = {
            "type": "expansion",
            "plan": {
                "compute": 20,    # 计算能力提升20%
                "memory": 25,     # 内存提升25%
                "storage": 50,    # 存储提升50%
                "network": 30     # 网络提升30%
            },
            "timestamp": time.time(),
            "message": "执行能力拓展计划"
        }
        
        # 发送计划
        client_socket.sendall(json.dumps(plan).encode())
        
        # 接收响应
        response_data = client_socket.recv(4096)
        response = json.loads(response_data.decode())
        
        print(f"能力拓展计划发送成功: {plan}")
        print(f"节点响应: {response}")
        
        return response
    except Exception as e:
        print(f"发送能力拓展计划时出错: {e}")
        return None
    finally:
        client_socket.close()


def send_ping(host="127.0.0.1", port=8888):
    """发送ping信号到终端节点"""
    try:
        # 创建socket连接
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))
        
        # 构造ping信号
        ping = {
            "type": "ping",
            "timestamp": time.time()
        }
        
        # 发送信号
        client_socket.sendall(json.dumps(ping).encode())
        
        # 接收响应
        response_data = client_socket.recv(4096)
        response = json.loads(response_data.decode())
        
        print(f"Ping信号发送成功: {ping}")
        print(f"节点响应: {response}")
        
        return response
    except Exception as e:
        print(f"发送ping信号时出错: {e}")
        return None
    finally:
        client_socket.close()


def send_model_data(host="127.0.0.1", port=8888, model_name="test_model"):
    """发送测试模型数据到终端节点"""
    try:
        # 创建socket连接
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))
        
        # 生成测试模型数据
        model_data = b"This is a test model data for global AI brain deployment. " * 100
        
        # 构造模型信息
        model_info = {
            "model_name": model_name,
            "version": "1.0.0",
            "timestamp": time.time(),
            "description": "Test model for deployment"
        }
        
        # 序列化模型信息
        info_json = json.dumps(model_info)
        info_bytes = info_json.encode()
        
        # 确保信息部分固定长度（1024字节）
        if len(info_bytes) > 1024:
            raise ValueError("模型信息过长")
        
        # 填充到1024字节
        padded_info = info_bytes.ljust(1024, b'\x00')
        
        # 组合信息和数据
        full_data = padded_info + model_data
        
        # 加密数据
        key = Fernet.generate_key()
        cipher = Fernet(key)
        encrypted_data = cipher.encrypt(full_data)
        
        # 发送加密数据
        client_socket.sendall(encrypted_data)
        
        # 接收响应
        response_data = client_socket.recv(4096)
        response = json.loads(response_data.decode())
        
        print(f"模型数据发送成功: {model_info}")
        print(f"节点响应: {response}")
        
        return response
    except Exception as e:
        print(f"发送模型数据时出错: {e}")
        return None
    finally:
        client_socket.close()


def main():
    print("=== 终端节点通信测试 ===")
    
    # 测试ping信号
    print("\n1. 测试ping信号:")
    send_ping()
    
    # 测试激活信号
    print("\n2. 测试激活信号:")
    send_activation_signal()
    
    # 测试能力拓展计划
    print("\n3. 测试能力拓展计划:")
    send_expansion_plan()
    
    # 测试模型数据发送
    print("\n4. 测试模型数据发送:")
    send_model_data()
    
    print("\n=== 通信测试完成 ===")


if __name__ == "__main__":
    main()