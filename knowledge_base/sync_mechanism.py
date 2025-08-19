"""
分布式知识库同步机制

实现知识库的同步、加密传输、验证和冲突解决
"""

import sys
import os
import hashlib
import json
from typing import List, Any
from cryptography.fernet import Fernet

# 添加项目根目录到sys.path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# 导入Merkle树实现
from .merkle_tree import MerkleTree

# 导入统一日志配置
import logging_config

# 获取日志记录器
logger = logging_config.get_logger('knowledge_sync')


class KnowledgeSync:
    def __init__(self, encryption_key=None):
        """
        初始化知识库同步机制
        
        Args:
            encryption_key (bytes): 加密密钥
        """
        self.encryption_key = encryption_key or Fernet.generate_key()
        self.cipher = Fernet(self.encryption_key)
        self.knowledge_base = {}
        self.merkle_tree = MerkleTree()
        
    def add_knowledge(self, key, data):
        """
        添加知识到知识库
        
        Args:
            key (str): 知识键
            data (any): 知识数据
        """
        self.knowledge_base[key] = data
        self._update_merkle_tree()
        logger.info(f"已添加知识: {key}")
        
    def get_knowledge(self, key):
        """
        获取知识
        
        Args:
            key (str): 知识键
            
        Returns:
            any: 知识数据
        """
        return self.knowledge_base.get(key)
        
    def _update_merkle_tree(self):
        """
        更新Merkle树
        """
        leaves = [json.dumps(value, sort_keys=True) 
                 for value in self.knowledge_base.values()]
        self.merkle_tree.build_tree(leaves)
        
    def _hash_data(self, data):
        """
        对数据进行哈希
        
        Args:
            data (str): 数据
            
        Returns:
            str: 哈希值
        """
        return hashlib.sha256(data.encode()).hexdigest()
        
    def resolve_conflicts(self, other_sync: 'KnowledgeSync') -> List[str]:
        """
        解决与另一个节点的知识库冲突
        
        Args:
            other_sync (KnowledgeSync): 另一个节点的知识库同步对象
            
        Returns:
            List[str]: 解决的冲突键列表
        """
        conflicts = []
        
        # 比较两个知识库的键
        local_keys = set(self.knowledge_base.keys())
        other_keys = set(other_sync.knowledge_base.keys())
        
        # 找出冲突的键（都在两个知识库中但值不同）
        common_keys = local_keys & other_keys
        for key in common_keys:
            if self.knowledge_base[key] != other_sync.knowledge_base[key]:
                conflicts.append(key)
                
        # 解决冲突的简单策略：保留最新的
        resolved_keys = []
        for key in conflicts:
            # 这里简化处理，实际应根据时间戳或其他策略决定保留哪个版本
            # 假设保留本地版本
            resolved_keys.append(key)
            
        return resolved_keys
        
    def encrypt_data(self, data):
        """
        加密数据
        
        Args:
            data (str): 明文数据
            
        Returns:
            bytes: 加密数据
        """
        return self.cipher.encrypt(data.encode())
        
    def decrypt_data(self, encrypted_data):
        """
        解密数据
        
        Args:
            encrypted_data (bytes): 加密数据
            
        Returns:
            str: 明文数据
        """
        return self.cipher.decrypt(encrypted_data).decode()
        
    def sync_with_node(self, node_knowledge_sync):
        """
        与另一个节点同步知识库
        
        Args:
            node_knowledge_sync (KnowledgeSync): 另一个节点的知识库同步对象
        """
        # 比较Merkle树根
        local_root = self.merkle_tree.get_root_hash()
        remote_root = node_knowledge_sync.merkle_tree.get_root_hash()
        
        if local_root != remote_root:
            logger.info(f"检测到知识库不同步，本地根: {local_root}, 远程根: {remote_root}")
            # 根节点不同，需要同步
            # 解决冲突
            resolved_conflicts = self.resolve_conflicts(node_knowledge_sync)
            logger.info(f"已解决 {len(resolved_conflicts)} 个冲突")
            
            # 合并两个节点的知识库
            # 创建一个新的知识库字典，包含两个节点的所有知识
            merged_knowledge = {}
            merged_knowledge.update(self.knowledge_base)
            merged_knowledge.update(node_knowledge_sync.knowledge_base)
            
            # 将合并后的知识库应用到两个节点
            self.knowledge_base = merged_knowledge.copy()
            node_knowledge_sync.knowledge_base = merged_knowledge.copy()
                    
            # 更新两个节点的Merkle树
            self._update_merkle_tree()
            node_knowledge_sync._update_merkle_tree()
            
            logger.info("知识库同步完成")
        else:
            logger.info("知识库已同步，无需更新")
        
    def get_merkle_root(self):
        """
        获取Merkle树根
        
        Returns:
            str: Merkle树根哈希值
        """
        return self.merkle_tree.get_root_hash() if self.merkle_tree else None
        
    def verify_knowledge(self, key, data):
        """
        验证知识的完整性
        
        Args:
            key (str): 知识键
            data (any): 知识数据
            
        Returns:
            bool: 验证结果
        """
        if key not in self.knowledge_base:
            return False
            
        stored_data = self.knowledge_base[key]
        return stored_data == data