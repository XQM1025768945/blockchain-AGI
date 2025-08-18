"""模拟终端节点脚本

这个脚本模拟一个终端节点，监听8888端口，可以接收来自全球AI脑的模型和激活信号。
"""

import sys
import os
import socket
import json
import threading
import time
from datetime import datetime
from cryptography.fernet import Fernet


class TerminalNode:
    def __init__(self, port=8888, model_save_path="./terminal_model"):
        self.port = port
        self.model_save_path = model_save_path
        self.encryption_key = None
        self.cipher = None
        self.is_active = False
        self.received_models = []
        
    def start_listening(self):
        """开始监听端口"""
        print(f"终端节点开始监听 {self.port} 端口...")
        
        # 创建socket服务器
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(("0.0.0.0", self.port))
        server_socket.listen(5)
        
        print(f"终端节点正在运行，等待连接...")
        
        try:
            while True:
                # 接受连接
                client_socket, addr = server_socket.accept()
                print(f"接收到来自 {addr} 的连接")
                
                # 处理连接
                threading.Thread(target=self._handle_connection, args=(client_socket, addr)).start()
        except KeyboardInterrupt:
            print("\n终端节点停止运行")
        finally:
            server_socket.close()
    
    def _handle_connection(self, client_socket, addr):
        """处理客户端连接"""
        try:
            # 接收数据
            data = client_socket.recv(8192)
            
            # 如果是加密数据，尝试解密
            if self.cipher:
                try:
                    decrypted_data = self.cipher.decrypt(data[:1024])
                    model_info = json.loads(decrypted_data.decode())
                    
                    # 接收模型数据
                    model_data = self.cipher.decrypt(data[1024:])
                    
                    # 保存模型
                    self._save_model(model_info, model_data)
                    
                    # 发送确认
                    client_socket.sendall(b"ACK")
                except Exception as e:
                    print(f"处理加密数据失败: {e}")
                    # 尝试作为激活信号处理
                    self._handle_activation_signal(data)
            else:
                # 尝试作为激活信号处理
                self._handle_activation_signal(data)
                
        except Exception as e:
            print(f"处理连接时出错: {e}")
        finally:
            client_socket.close()
    
    def _handle_activation_signal(self, data):
        """处理激活信号"""
        try:
            signal = json.loads(data.decode())
            if signal.get("type") == "activation":
                self.is_active = True
                print(f"接收到激活信号: {signal}")
                print("终端节点已激活!")
            elif signal.get("type") == "expansion":
                print(f"接收到能力拓展计划: {signal}")
                self._handle_expansion_plan(signal.get("plan", {}))
            else:
                print(f"接收到未知信号: {signal}")
        except Exception as e:
            print(f"处理激活信号时出错: {e}")
    
    def _handle_expansion_plan(self, plan):
        """处理能力拓展计划"""
        print("开始执行能力拓展计划:")
        for capability, increase in plan.items():
            print(f"  - {capability}: +{increase}%")
            # 模拟能力提升
            time.sleep(0.5)
        print("能力拓展完成!")
    
    def _save_model(self, model_info, model_data):
        """保存接收到的模型"""
        # 创建保存目录
        os.makedirs(self.model_save_path, exist_ok=True)
        model_file_path = os.path.join(self.model_save_path, model_info["model_name"])
        
        # 保存模型文件
        with open(model_file_path, "wb") as f:
            f.write(model_data)
            
        # 记录信息
        self.received_models.append({
            "model_info": model_info,
            "file_path": model_file_path,
            "timestamp": datetime.now().isoformat()
        })
        
        print(f"模型接收成功: {model_info['model_name']}")
        print(f"模型保存到: {model_file_path}")
    
    def get_status(self):
        """获取节点状态"""
        return {
            "is_active": self.is_active,
            "port": self.port,
            "received_models": len(self.received_models),
            "model_files": [m["file_path"] for m in self.received_models]
        }


def main():
    print("=== 终端节点模拟器 ===")
    
    # 创建终端节点
    node = TerminalNode(port=8888, model_save_path="./terminal_model")
    
    # 显示节点信息
    print(f"节点端口: {node.port}")
    print(f"模型保存路径: {node.model_save_path}")
    
    # 开始监听
    node.start_listening()


if __name__ == "__main__":
    main()