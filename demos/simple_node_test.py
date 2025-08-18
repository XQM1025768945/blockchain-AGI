"""简化版终端节点测试脚本

这个脚本将启动一个简单的终端节点并测试基本通信功能。
"""

import socket
import json
import time
import threading


class SimpleTerminalNode:
    def __init__(self, host="127.0.0.1", port=8888):
        self.host = host
        self.port = port
        self.running = False
        
    def start(self):
        """启动终端节点"""
        print(f"启动终端节点 {self.host}:{self.port}...")
        
        # 创建socket服务器
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((self.host, self.port))
        server_socket.listen(5)
        
        self.running = True
        print("终端节点已启动，等待连接...")
        
        try:
            while self.running:
                # 接受连接（设置超时以允许检查running状态）
                server_socket.settimeout(1.0)
                try:
                    client_socket, addr = server_socket.accept()
                    print(f"接收到来自 {addr} 的连接")
                    
                    # 处理连接
                    self._handle_connection(client_socket)
                except socket.timeout:
                    continue
        except Exception as e:
            print(f"服务器错误: {e}")
        finally:
            server_socket.close()
            print("终端节点已停止")
    
    def stop(self):
        """停止终端节点"""
        self.running = False
    
    def _handle_connection(self, client_socket):
        """处理客户端连接"""
        try:
            # 接收数据
            data = client_socket.recv(4096)
            
            # 尝试解析为JSON
            try:
                signal = json.loads(data.decode())
                signal_type = signal.get("type")
                
                if signal_type == "ping":
                    response = {"status": "success", "message": "pong"}
                    client_socket.sendall(json.dumps(response).encode())
                elif signal_type == "activation":
                    response = {"status": "success", "message": "节点已激活"}
                    client_socket.sendall(json.dumps(response).encode())
                else:
                    response = {"status": "unknown", "message": "未知信号类型"}
                    client_socket.sendall(json.dumps(response).encode())
            except json.JSONDecodeError:
                response = {"status": "error", "message": "无效的JSON数据"}
                client_socket.sendall(json.dumps(response).encode())
                
        except Exception as e:
            print(f"处理连接时出错: {e}")
        finally:
            client_socket.close()


def test_communication():
    """测试通信功能"""
    print("测试通信功能...")
    
    # 测试ping信号
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(("127.0.0.1", 8888))
        
        ping_signal = {"type": "ping", "timestamp": time.time()}
        client_socket.sendall(json.dumps(ping_signal).encode())
        
        response_data = client_socket.recv(4096)
        response = json.loads(response_data.decode())
        
        print(f"Ping测试结果: {response}")
        client_socket.close()
    except Exception as e:
        print(f"Ping测试失败: {e}")
        return False
    
    # 测试激活信号
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(("127.0.0.1", 8888))
        
        activation_signal = {"type": "activation", "timestamp": time.time()}
        client_socket.sendall(json.dumps(activation_signal).encode())
        
        response_data = client_socket.recv(4096)
        response = json.loads(response_data.decode())
        
        print(f"激活测试结果: {response}")
        client_socket.close()
    except Exception as e:
        print(f"激活测试失败: {e}")
        return False
    
    return True


def main():
    print("=== 简化版终端节点测试 ===")
    
    # 创建并启动终端节点
    node = SimpleTerminalNode()
    
    # 在单独的线程中启动节点
    node_thread = threading.Thread(target=node.start, daemon=True)
    node_thread.start()
    
    # 等待节点启动
    time.sleep(2)
    
    # 测试通信
    success = test_communication()
    
    # 停止节点
    node.stop()
    
    if success:
        print("\n通信测试成功!")
    else:
        print("\n通信测试失败!")
    
    print("=== 测试完成 ===")


if __name__ == "__main__":
    main()