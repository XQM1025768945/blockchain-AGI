"""
自我复制机制

实现节点发现、模型传输和验证协议
"""

import os
import sys
import json
import hashlib
import socket
import ssl
import threading
import time
import concurrent.futures
from datetime import datetime
from typing import Dict, List, Set, Tuple, Any
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import logging_config

# 设置日志配置
logger = logging_config.get_logger('self_replication')


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
        self.iv = os.urandom(16)
        self.cipher = Fernet(self.encryption_key)
        
    def discover_nodes(self, base_ip="192.168.1.", start=2, end=254, port=8888):
        """
        发现网络中的其他节点。
        """
        nodes = set()
        # 使用多线程提高节点发现效率
        import concurrent.futures
        with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
            futures = []
            for i in range(start, end + 1):
                ip = f"{base_ip}{i}"
                futures.append(executor.submit(self._check_node, ip, port))
            
            for future in concurrent.futures.as_completed(futures):
                node = future.result()
                if node:
                    nodes.add(node)
        
        self.nodes.update(nodes)
        logger.info(f"发现节点: {nodes}")
        return list(nodes)

    def _check_node(self, ip, port):
        """
        检查单个节点是否可用。
        """
        if self._is_port_open(ip, port):
            return (ip, port)
        return None
        
    def _is_port_open(self, ip, port, timeout=3):
        """
        检查指定IP和端口是否开放。
        """
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((ip, port))
            sock.close()
            return result == 0
        except:
            return False

    def check_node_health(self, ip, port, timeout=5):
        """
        检查节点健康状态。
        """
        try:
            # 发送健康检查请求
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.settimeout(timeout)
            client_socket.connect((ip, port))
            
            # 发送健康检查消息
            import pickle
            health_check_msg = {"action": "health_check"}
            encrypted_msg = self.encrypt_data(pickle.dumps(health_check_msg))
            client_socket.send(encrypted_msg)
            
            # 接收响应
            response = client_socket.recv(1024)
            decrypted_response = self.decrypt_data(response)
            response_data = pickle.loads(decrypted_response)
            
            client_socket.close()
            
            return response_data.get("status") == "healthy"
        except Exception as e:
            logger.error(f"健康检查 {ip}:{port} 失败: {e}")
            return False
        
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

    def encrypt_data(self, data):
        cipher = Cipher(algorithms.AES(self.encryption_key), modes.CFB(self.iv), backend=default_backend())
        encryptor = cipher.encryptor()
        return encryptor.update(data) + encryptor.finalize()

    def decrypt_data(self, encrypted_data):
        cipher = Cipher(algorithms.AES(self.encryption_key), modes.CFB(self.iv), backend=default_backend())
        decryptor = cipher.decryptor()
        return decryptor.update(encrypted_data) + decryptor.finalize()
        
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
            
            # 分块传输模型数据
            chunk_size = 4096
            for i in range(0, len(model_data), chunk_size):
                chunk = model_data[i:i+chunk_size]
                # 加密数据块
                encrypted_chunk = self.encrypt_data(chunk)
                # 发送数据块大小
                sock.send(len(encrypted_chunk).to_bytes(4, byteorder='big'))
                # 发送加密的数据块
                sock.sendall(encrypted_chunk)
            
            # 发送结束标记
            sock.send((0).to_bytes(4, byteorder='big'))
                    
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
            
            logger.info(f"模型已发送到 {target_ip}:{target_port}")
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
            
            logger.error(f"发送模型到 {target_ip}:{target_port} 失败: {e}")
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
            
            logger.info(f"开始监听 {listen_port} 端口...")
            
            while True:
                # 接受连接
                client_socket, addr = server_socket.accept()
                logger.info(f"接收到来自 {addr} 的连接")
                # Wrap socket with SSL
                context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
                context.load_cert_chain(certfile="cert.pem", keyfile="key.pem")
                secure_conn = context.wrap_socket(client_socket, server_side=True)
                
                # 接收加密的模型信息
                encrypted_info = client_socket.recv(1024)
                info_data = self.cipher.decrypt(encrypted_info)
                model_info = json.loads(info_data.decode())
                
                # 创建保存目录
                os.makedirs(save_path, exist_ok=True)
                model_file_path = os.path.join(save_path, model_info["model_name"])
                
                # 接收模型数据块
                model_data = b''
                while True:
                    # 接收数据块大小
                    chunk_size_bytes = client_socket.recv(4)
                    if len(chunk_size_bytes) == 0:
                        break
                    chunk_size = int.from_bytes(chunk_size_bytes, byteorder='big')
                    if chunk_size == 0:
                        break
                    # 接收加密的数据块
                    encrypted_chunk = client_socket.recv(chunk_size)
                    # 解密数据块
                    chunk = self.decrypt_data(encrypted_chunk)
                    model_data += chunk
                
                # 保存模型文件
                with open(model_file_path, "wb") as f:
                    f.write(model_data)
                        
                client_socket.close()
                
                # 验证模型
                with open(model_file_path, "rb") as f:
                    received_hash = hashlib.sha256(f.read()).hexdigest()
                    
                if received_hash == model_info["model_hash"]:
                    logger.info(f"模型接收成功并验证通过: {model_file_path}")
                    
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
                    logger.error(f"模型接收失败，哈希验证不通过")
                    
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
            logger.error(f"接收模型失败: {e}")
            
            # 记录日志
            self.replication_log.append({
                "action": "receive_model",
                "timestamp": datetime.now(),
                "status": "failed",
                "error": str(e)
            })
            
    def replicate_to_all_nodes(self, model_path=None, max_retries=3):
        """
        将模型复制到所有发现的节点。
        """
        if model_path:
            self.model_path = model_path
        
        if not self.nodes:
            logger.warning("没有发现任何节点")
            return
            
        logger.info(f"开始向 {len(self.nodes)} 个节点复制模型...")
        
        success_count = 0
        failed_nodes = []
        
        for node_ip in self.nodes:
            success = False
            for attempt in range(max_retries):
                try:
                    if self.send_model(node_ip, self.port):
                        success = True
                        success_count += 1
                        break
                except Exception as e:
                    logger.warning(f"第{attempt+1}次尝试发送模型到 {node_ip}:{self.port} 失败: {e}")
                    time.sleep(2 ** attempt)  # 指数退避
            
            if not success:
                failed_nodes.append(node_ip)
                logger.error(f"无法将模型发送到 {node_ip}:{self.port}，已达到最大重试次数")
        
        if failed_nodes:
            logger.error(f"以下节点发送失败: {failed_nodes}")
        else:
            logger.info("所有节点复制完成")
        
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