"""增强版终端节点模拟脚本

这个脚本模拟一个功能更完整的终端节点，支持接收模型、激活信号和能力拓展计划。
"""

import sys
import os
import socket
import json
import threading
import time
from datetime import datetime
from cryptography.fernet import Fernet


class EnhancedTerminalNode:
    def __init__(self, host="127.0.0.1", port=8888, model_save_path="./terminal_model"):
        self.host = host
        self.port = port
        self.model_save_path = model_save_path
        self.encryption_key = Fernet.generate_key()
        self.cipher = Fernet(self.encryption_key)
        self.is_active = False
        self.received_models = []
        self.capabilities = {
            "compute": 50.0,
            "memory": 16.0,
            "storage": 256.0,
            "network": 100.0
        }
        self.running = False
        
    def start_listening(self):
        """开始监听端口"""
        print(f"终端节点开始监听 {self.host}:{self.port}...")
        
        # 创建socket服务器
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((self.host, self.port))
        server_socket.listen(5)
        
        self.running = True
        print(f"终端节点正在运行，等待连接...")
        
        try:
            while self.running:
                # 接受连接（设置超时以允许检查running状态）
                server_socket.settimeout(1.0)
                try:
                    client_socket, addr = server_socket.accept()
                    print(f"接收到来自 {addr} 的连接")
                    
                    # 处理连接
                    threading.Thread(target=self._handle_connection, args=(client_socket, addr), daemon=True).start()
                except socket.timeout:
                    continue
        except Exception as e:
            print(f"服务器错误: {e}")
        finally:
            server_socket.close()
            print("终端节点已停止")
    
    def stop_listening(self):
        """停止监听"""
        self.running = False
    
    def _handle_connection(self, client_socket, addr):
        """处理客户端连接"""
        try:
            # 接收数据
            data = client_socket.recv(8192)
            
            # 尝试解密数据
            try:
                decrypted_data = self.cipher.decrypt(data)
                # 如果解密成功，这应该是模型数据
                self._handle_model_data(decrypted_data, client_socket)
            except Exception:
                # 如果解密失败，这可能是JSON信号
                self._handle_json_signal(data, client_socket)
                
        except Exception as e:
            print(f"处理连接时出错: {e}")
        finally:
            client_socket.close()
    
    def _handle_model_data(self, data, client_socket):
        """处理模型数据"""
        try:
            # 解析数据（假设前1024字节是模型信息，其余是模型数据）
            if len(data) > 1024:
                info_data = data[:1024].rstrip(b'\x00')  # 移除填充的空字节
                model_data = data[1024:]
                
                # 解析模型信息
                model_info = json.loads(info_data.decode())
                
                # 保存模型
                self._save_model(model_info, model_data)
                
                # 发送确认
                response = {"status": "success", "message": "模型接收成功"}
                client_socket.sendall(json.dumps(response).encode())
            else:
                # 尝试解析为JSON
                signal = json.loads(data.decode())
                self._handle_json_signal(data, client_socket)
        except Exception as e:
            print(f"处理模型数据时出错: {e}")
            response = {"status": "error", "message": str(e)}
            client_socket.sendall(json.dumps(response).encode())
    
    def _handle_json_signal(self, data, client_socket):
        """处理JSON信号"""
        try:
            signal = json.loads(data.decode())
            signal_type = signal.get("type")
            
            if signal_type == "activation":
                self._handle_activation_signal(signal, client_socket)
            elif signal_type == "expansion":
                self._handle_expansion_plan(signal.get("plan", {}), client_socket)
            elif signal_type == "ping":
                self._handle_ping(client_socket)
            else:
                print(f"接收到未知信号: {signal}")
                response = {"status": "unknown", "message": "未知信号类型"}
                client_socket.sendall(json.dumps(response).encode())
        except Exception as e:
            print(f"处理JSON信号时出错: {e}")
            response = {"status": "error", "message": str(e)}
            client_socket.sendall(json.dumps(response).encode())
    
    def _handle_activation_signal(self, signal, client_socket):
        """处理激活信号"""
        self.is_active = True
        print(f"接收到激活信号: {signal}")
        print("终端节点已激活!")
        
        response = {
            "status": "success", 
            "message": "节点已激活",
            "node_info": {
                "is_active": self.is_active,
                "capabilities": self.capabilities
            }
        }
        client_socket.sendall(json.dumps(response).encode())
    
    def _handle_expansion_plan(self, plan, client_socket):
        """处理能力拓展计划"""
        print("开始执行能力拓展计划:")
        for capability, increase in plan.items():
            if capability in self.capabilities:
                old_value = self.capabilities[capability]
                self.capabilities[capability] *= (1 + increase / 100)
                new_value = self.capabilities[capability]
                print(f"  - {capability}: {old_value:.2f} -> {new_value:.2f} (+{increase}%)")
            else:
                print(f"  - 未知能力项: {capability}")
        
        print("能力拓展完成!")
        
        response = {
            "status": "success", 
            "message": "能力拓展完成",
            "updated_capabilities": self.capabilities
        }
        client_socket.sendall(json.dumps(response).encode())
    
    def _handle_ping(self, client_socket):
        """处理ping信号"""
        print("接收到ping信号")
        response = {
            "status": "success", 
            "message": "pong",
            "node_info": {
                "is_active": self.is_active,
                "capabilities": self.capabilities
            }
        }
        client_socket.sendall(json.dumps(response).encode())
    
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
            "host": self.host,
            "port": self.port,
            "received_models": len(self.received_models),
            "model_files": [m["file_path"] for m in self.received_models],
            "capabilities": self.capabilities
        }


def main():
    print("=== 增强版终端节点模拟器 ===")
    
    # 创建终端节点
    node = EnhancedTerminalNode(host="127.0.0.1", port=8888, model_save_path="./terminal_model")
    
    # 显示节点信息
    print(f"节点地址: {node.host}:{node.port}")
    print(f"模型保存路径: {node.model_save_path}")
    
    # 在单独的线程中启动监听
    listener_thread = threading.Thread(target=node.start_listening, daemon=True)
    listener_thread.start()
    
    # 等待用户输入以停止
    print("\n按 Enter 键停止节点...")
    input()
    
    # 停止节点
    node.stop_listening()
    print("终端节点已停止")


if __name__ == "__main__":
    main()