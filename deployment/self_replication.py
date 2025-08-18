"""
自我复制机制

实现节点发现、模型传输和验证协议
"""

import os
import json
import hashlib
import socket
import threading
import time
from datetime import datetime
from typing import List
from cryptography.fernet import Fernet


class SelfReplication:
    def __init__(self, model_path, port=8888, encryption_key=None):
        """
        初始化自我复制机制
        
        Args:
            model_path (str): 模型文件路径
            port (int): 监听端口
            encryption_key (bytes): 加密密钥
        """
        self.model_path = model_path
        self.port = port
        self.nodes = set()
        self.replication_log = []
        self.encryption_key = encryption_key or Fernet.generate_key()
        self.cipher = Fernet(self.encryption_key)
        
    def discover_nodes(self, network_range="192.168.1", port=8888, timeout=5):
        """
        发现网络中的节点
        
        Args:
            network_range (str): 网络范围
            port (int): 端口
            timeout (int): 超时时间
        """
        print(f"开始发现节点... ({network_range}.1-{network_range}.254:{port})")
        
        def check_host(ip, port, timeout):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(timeout)
                result = sock.connect_ex((ip, port))
                sock.close()
                if result == 0:
                    self.nodes.add(ip)
                    print(f"发现节点: {ip}:{port}")
            except:
                pass
                
        # 创建线程检查每个IP
        threads = []
        for i in range(1, 255):
            ip = f"{network_range}.{i}"
            thread = threading.Thread(target=check_host, args=(ip, port, timeout))
            threads.append(thread)
            thread.start()
            
        # 等待所有线程完成
        for thread in threads:
            thread.join()
            
        # 记录日志
        self.replication_log.append({
            "action": "discovery",
            "network_range": network_range,
            "port": port,
            "nodes_found": list(self.nodes),
            "timestamp": datetime.now(),
            "status": "completed"
        })
        
        print(f"节点发现完成，共发现 {len(self.nodes)} 个节点")
        
    def calculate_model_hash(self):
        """
        计算模型文件哈希
        
        Returns:
            str: 模型哈希值
        """
        if not os.path.exists(self.model_path):
            return None
            
        with open(self.model_path, "rb") as f:
            model_data = f.read()
            model_hash = hashlib.sha256(model_data).hexdigest()
            
        return model_hash
        
    def send_model(self, target_ip, target_port=8888):
        """
        向目标节点发送模型
        
        Args:
            target_ip (str): 目标IP
            target_port (int): 目标端口
        """
        try:
            import socket
            
            # 创建socket连接
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((target_ip, target_port))
            
            # 准备模型数据
            with open(self.model_path, "rb") as f:
                model_data = f.read()
            
            # 发送模型信息
            model_info = {
                "model_name": os.path.basename(self.model_path),
                "model_size": len(model_data),
                "model_hash": self.calculate_model_hash()
            }
            
            # 发送加密的模型信息
            encrypted_info = self.cipher.encrypt(json.dumps(model_info).encode())
            sock.sendall(encrypted_info)
            
            # 加密模型数据
            encrypted_data = self.cipher.encrypt(model_data)
            
            # 发送加密的模型数据
            sock.sendall(encrypted_data)
                    
            sock.close()
            
            # 记录日志
            self.replication_log.append({
                "action": "send_model",
                "target_ip": target_ip,
                "target_port": target_port,
                "model_info": model_info,
                "timestamp": datetime.now(),
                "status": "success"
            })
            
            print(f"模型已发送到 {target_ip}:{target_port}")
            return True
        except Exception as e:
            # 记录日志
            self.replication_log.append({
                "action": "send_model",
                "target_ip": target_ip,
                "target_port": target_port,
                "timestamp": datetime.now(),
                "status": "failed",
                "error": str(e)
            })
            
            print(f"发送模型到 {target_ip}:{target_port} 失败: {e}")
            return False
            
    def receive_model(self, save_path="./received_model", listen_port=8888):
        """
        接收来自其他节点的模型
        
        Args:
            save_path (str): 保存路径
            listen_port (int): 监听端口
        """
        try:
            import socket
            
            # 创建socket服务器
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.bind(("0.0.0.0", listen_port))
            server_socket.listen(5)
            
            print(f"开始监听 {listen_port} 端口...")
            
            while True:
                # 接受连接
                client_socket, addr = server_socket.accept()
                print(f"接收到来自 {addr} 的连接")
                
                # 接收加密的模型信息
                encrypted_info = client_socket.recv(1024)
                info_data = self.cipher.decrypt(encrypted_info)
                model_info = json.loads(info_data.decode())
                
                # 创建保存目录
                os.makedirs(save_path, exist_ok=True)
                model_file_path = os.path.join(save_path, model_info["model_name"])
                
                # 接收加密的模型数据
                encrypted_data = client_socket.recv(4096)
                model_data = self.cipher.decrypt(encrypted_data)
                
                # 保存模型文件
                with open(model_file_path, "wb") as f:
                    f.write(model_data)
                        
                client_socket.close()
                
                # 验证模型
                with open(model_file_path, "rb") as f:
                    received_hash = hashlib.sha256(f.read()).hexdigest()
                    
                if received_hash == model_info["model_hash"]:
                    print(f"模型接收成功并验证通过: {model_file_path}")
                    
                    # 记录日志
                    self.replication_log.append({
                        "action": "receive_model",
                        "source_ip": addr[0],
                        "source_port": addr[1],
                        "model_info": model_info,
                        "model_file": model_file_path,
                        "timestamp": datetime.now(),
                        "status": "success"
                    })
                else:
                    print(f"模型接收失败，哈希验证不通过")
                    
                    # 记录日志
                    self.replication_log.append({
                        "action": "receive_model",
                        "source_ip": addr[0],
                        "source_port": addr[1],
                        "model_info": model_info,
                        "model_file": model_file_path,
                        "timestamp": datetime.now(),
                        "status": "failed",
                        "error": "Hash verification failed"
                    })
                    
                # 只接收一次就退出
                break
                
            server_socket.close()
        except Exception as e:
            print(f"接收模型失败: {e}")
            
            # 记录日志
            self.replication_log.append({
                "action": "receive_model",
                "timestamp": datetime.now(),
                "status": "failed",
                "error": str(e)
            })
            
    def replicate_to_all_nodes(self):
        """
        向所有发现的节点复制模型
        """
        if not self.nodes:
            print("没有发现任何节点")
            return
            
        print(f"开始向 {len(self.nodes)} 个节点复制模型...")
        
        success_count = 0
        for node_ip in self.nodes:
            if self.send_model(node_ip, self.port):
                success_count += 1
                
        print(f"复制完成，成功 {success_count}/{len(self.nodes)} 个节点")
        
        # 记录日志
        self.replication_log.append({
            "action": "replicate_all",
            "total_nodes": len(self.nodes),
            "success_count": success_count,
            "timestamp": datetime.now(),
            "status": "completed"
        })
        
    def get_replication_log(self):
        """
        获取复制日志
        
        Returns:
            list: 复制日志
        """
        return self.replication_log
        
    def _enhanced_discover_nodes(self) -> List[str]:
        """
        增强的节点发现算法
        
        Returns:
            List[str]: 发现的节点列表
        """
        nodes = []
        
        # 扫描本地网络
        local_ip = socket.gethostbyname(socket.gethostname())
        base_ip = '.'.join(local_ip.split('.')[:-1]) + '.'
        
        # 扫描端口
        for i in range(1, 255):
            target_ip = base_ip + str(i)
            try:
                # 检查目标节点是否在线并监听复制端口
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(0.1)  # 设置短超时
                result = sock.connect_ex((target_ip, self.port))
                if result == 0:
                    nodes.append(target_ip)
                sock.close()
            except:
                pass
                
        # 去重
        return list(set(nodes))
        
    def get_network_topology(self) -> dict:
        """
        获取网络拓扑信息
        
        Returns:
            dict: 网络拓扑信息
        """
        nodes = self._enhanced_discover_nodes()
        
        # 简化实现，实际应包含更多网络信息
        return {
            "discovered_nodes": nodes,
            "total_nodes": len(nodes),
            "timestamp": time.time()
        }