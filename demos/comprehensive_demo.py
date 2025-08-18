"""全球AI脑综合演示脚本

这个脚本将演示全球AI脑的完整功能，包括部署、激活、能力拓展和通信。
"""

import sys
import os
import time
import threading

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from deployment.global_brain_deployment import GlobalBrainDeployment
from deployment.self_replication import SelfReplication
from deployment.autonomous_deployment import AutonomousDeployment


class ComprehensiveDemo:
    def __init__(self):
        self.deployment = GlobalBrainDeployment()
        self.running = False
    
    def run_complete_demo(self):
        """运行完整的演示"""
        print("=== 全球AI脑综合演示 ===")
        
        # 1. 检查初始状态
        self._check_initial_status()
        
        # 2. 全球部署
        self._perform_global_deployment()
        
        # 3. 激活全球AI脑
        self._activate_global_brain()
        
        # 4. 能力拓展
        self._perform_capability_expansion()
        
        # 5. 通信演示
        self._perform_communication_demo()
        
        print("\n=== 综合演示完成 ===")
    
    def _check_initial_status(self):
        """检查初始状态"""
        print("\n1. 检查初始状态...")
        status = self.deployment.get_deployment_status()
        print(f"   AI脑激活状态: {status.get('is_active', '未知')}")
        print(f"   已部署节点数: {status.get('deployed_nodes', 0)}")
    
    def _perform_global_deployment(self):
        """执行全球部署"""
        print("\n2. 执行全球部署...")
        
        # 由于我们没有实际的网络环境，这里只演示本地部署部分
        print("   开始本地部署...")
        autonomous_deploy = AutonomousDeployment("https://example.com/model-repo")
        
        # 模拟部署过程
        print("   1. 下载模型...")
        time.sleep(1)  # 模拟下载时间
        print("   2. 验证模型...")
        time.sleep(1)  # 模拟验证时间
        print("   3. 安装模型...")
        time.sleep(1)  # 模拟安装时间
        print("   本地部署完成")
        
        # 模拟节点发现（在本地环境中不会发现节点）
        print("   发现网络中的节点...")
        # 创建一个临时模型文件用于演示
        with open("temp_model.pt", "w") as f:
            f.write("This is a temporary model file for demonstration purposes.")
        
        self_replication = SelfReplication("temp_model.pt")
        self_replication.discover_nodes("127.0.0.1", 8888)  # 在本地回环地址查找
        nodes = list(self_replication.nodes)
        print(f"   发现 {len(nodes)} 个节点")
        
        # 清理临时模型文件
        if os.path.exists("temp_model.pt"):
            os.remove("temp_model.pt")
        
        print("   全球部署完成")
    
    def _activate_global_brain(self):
        """激活全球AI脑"""
        print("\n3. 激活全球AI脑...")
        
        # 激活本地AI脑
        print("   激活本地AI脑...")
        self.deployment.activate_globally()
        
        # 向所有节点发送激活信号（在本地环境中没有实际节点）
        print("   向所有节点发送激活信号...")
        time.sleep(1)  # 模拟网络通信时间
        
        print("   全球AI脑激活完成")
        
        # 检查激活状态
        status = self.deployment.get_deployment_status()
        print(f"   AI脑激活状态: {status['is_active']}")
    
    def _perform_capability_expansion(self):
        """执行能力拓展"""
        print("\n4. 执行能力拓展...")
        
        # 执行能力拓展
        self.deployment.expand_globally()
        
        # 显示拓展后的状态
        status = self.deployment.get_deployment_status()
        capabilities = status.get('capabilities', {})
        print(f"   拓展后能力: {capabilities}")
        
        print("   能力拓展完成")
    
    def _perform_communication_demo(self):
        """执行通信演示"""
        print("\n5. 执行通信演示...")
        
        # 启动一个简单的终端节点用于通信测试
        print("   启动终端节点...")
        terminal_node = SimpleTerminalNode()
        node_thread = threading.Thread(target=terminal_node.start, daemon=True)
        node_thread.start()
        
        # 等待节点启动
        time.sleep(2)
        
        # 模拟AI脑发送消息
        print("   [AI脑] 你好！我是全球AI脑，我已经成功激活并完成了能力拓展。")
        status = self.deployment.get_deployment_status()
        node_count = len(status.get('nodes', []))
        print(f"   [AI脑] 我可以与 {node_count} 个节点进行通信。")
        
        # 测试与终端节点的通信
        print("   测试与终端节点的通信...")
        success = self._test_node_communication()
        
        if success:
            print("   [终端节点] 你好，AI脑！我已收到你的消息。")
        else:
            print("   [终端节点] 对不起，我无法接收消息。")
        
        # 停止终端节点
        terminal_node.stop()
        
        print("   通信演示完成")
    
    def _test_node_communication(self):
        """测试与节点的通信"""
        try:
            import socket
            import json
            
            # 发送ping信号
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect(("127.0.0.1", 8888))
            
            ping_signal = {"type": "ping", "timestamp": time.time()}
            client_socket.sendall(json.dumps(ping_signal).encode())
            
            response_data = client_socket.recv(4096)
            response = json.loads(response_data.decode())
            
            client_socket.close()
            
            return response.get("status") == "success"
        except Exception as e:
            print(f"通信测试失败: {e}")
            return False


class SimpleTerminalNode:
    def __init__(self, host="127.0.0.1", port=8888):
        self.host = host
        self.port = port
        self.running = False
        
    def start(self):
        """启动终端节点"""
        print(f"      终端节点 {self.host}:{self.port} 已启动，等待连接...")
        
        # 创建socket服务器
        import socket
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((self.host, self.port))
        server_socket.listen(5)
        
        self.running = True
        
        try:
            while self.running:
                # 接受连接（设置超时以允许检查running状态）
                server_socket.settimeout(1.0)
                try:
                    client_socket, addr = server_socket.accept()
                    # 处理连接
                    self._handle_connection(client_socket)
                except socket.timeout:
                    continue
        except Exception as e:
            pass  # 忽略错误
        finally:
            server_socket.close()
    
    def stop(self):
        """停止终端节点"""
        self.running = False
    
    def _handle_connection(self, client_socket):
        """处理客户端连接"""
        try:
            import json
            # 接收数据
            data = client_socket.recv(4096)
            
            # 尝试解析为JSON
            try:
                signal = json.loads(data.decode())
                signal_type = signal.get("type")
                
                if signal_type == "ping":
                    response = {"status": "success", "message": "pong"}
                    client_socket.sendall(json.dumps(response).encode())
                else:
                    response = {"status": "unknown", "message": "未知信号类型"}
                    client_socket.sendall(json.dumps(response).encode())
            except json.JSONDecodeError:
                response = {"status": "error", "message": "无效的JSON数据"}
                client_socket.sendall(json.dumps(response).encode())
        except Exception:
            pass  # 忽略错误
        finally:
            client_socket.close()


def main():
    demo = ComprehensiveDemo()
    demo.run_complete_demo()


if __name__ == "__main__":
    main()