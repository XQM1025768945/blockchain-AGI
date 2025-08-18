"""
元学习云共享平台

实现元知识的共享、隐私保护和版本管理
"""

import hashlib
import json
import re
from datetime import datetime
from cryptography.fernet import Fernet


class MetaLearningPlatform:
    def __init__(self, encryption_key=None):
        """
        初始化元学习平台
        
        Args:
            encryption_key (bytes): 加密密钥
        """
        self.encryption_key = encryption_key or Fernet.generate_key()
        self.cipher = Fernet(self.encryption_key)
        self.meta_knowledge_base = {}
        self.access_control = {}
        self.version_history = {}
        
    def add_meta_knowledge(self, key, data, owner, permissions=None):
        """
        添加元知识
        
        Args:
            key (str): 元知识键
            data (any): 元知识数据
            owner (str): 所有者
            permissions (dict): 访问权限
        """
        # 加密数据
        encrypted_data = self.cipher.encrypt(json.dumps(data).encode())
        
        # 创建元知识条目
        meta_entry = {
            "data": encrypted_data,
            "owner": owner,
            "permissions": permissions or {"read": [owner], "write": [owner]},
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
            "version": 1
        }
        
        # 数据隐私保护
        protected_data = self._protect_data_privacy(data, 'internal')
        encrypted_data = self.cipher.encrypt(json.dumps(protected_data).encode())
        
        meta_entry['data'] = encrypted_data
        meta_entry['privacy_level'] = 'internal'
        
        self.meta_knowledge_base[key] = meta_entry
        self.version_history[key] = [meta_entry]
        
        # 更新访问控制
        self.access_control[key] = meta_entry["permissions"]
        
    def get_meta_knowledge(self, key, user):
        """
        获取元知识
        
        Args:
            key (str): 元知识键
            user (str): 请求用户
            
        Returns:
            any: 解密后的元知识数据
        """
        if key not in self.meta_knowledge_base:
            raise Exception(f"元知识 {key} 不存在")
            
        entry = self.meta_knowledge_base[key]
        
        # 检查读权限
        if "read" in entry["permissions"] and user not in entry["permissions"]["read"]:
            raise Exception(f"用户 {user} 没有读取权限")
            
        # 解密数据
        decrypted_data = self.cipher.decrypt(entry["data"]).decode()
        data = json.loads(decrypted_data)
        
        # 根据隐私级别进一步处理
        if 'privacy_level' in entry:
            privacy_level = entry['privacy_level']
            data = self._apply_privacy_filters(data, privacy_level)
            
        return data
        
    def update_meta_knowledge(self, key, data, user):
        """
        更新元知识
        
        Args:
            key (str): 元知识键
            data (any): 新的元知识数据
            user (str): 请求用户
        """
        if key not in self.meta_knowledge_base:
            raise Exception(f"元知识 {key} 不存在")
            
        entry = self.meta_knowledge_base[key]
        
        # 检查写权限
        if "write" in entry["permissions"] and user not in entry["permissions"]["write"]:
            raise Exception(f"用户 {user} 没有写入权限")
            
        # 加密新数据
        encrypted_data = self.cipher.encrypt(json.dumps(data).encode())
        
        # 更新条目
        new_version = entry["version"] + 1
        new_entry = {
            "data": encrypted_data,
            "owner": entry["owner"],
            "permissions": entry["permissions"],
            "created_at": entry["created_at"],
            "updated_at": datetime.now(),
            "version": new_version
        }
        
        self.meta_knowledge_base[key] = new_entry
        
        # 添加到版本历史
        if key in self.version_history:
            self.version_history[key].append(new_entry)
        else:
            self.version_history[key] = [new_entry]
            
    def get_version_history(self, key):
        """
        获取元知识的版本历史
        
        Args:
            key (str): 元知识键
            
        Returns:
            list: 版本历史
        """
        return self.version_history.get(key, [])
        
    def share_meta_knowledge(self, key, shared_with, permissions, owner):
        """
        共享元知识
        
        Args:
            key (str): 元知识键
            shared_with (list): 共享给的用户列表
            permissions (dict): 权限设置
            owner (str): 所有者
        """
        if key not in self.meta_knowledge_base:
            raise Exception(f"元知识 {key} 不存在")
            
        entry = self.meta_knowledge_base[key]
        
        # 检查所有权
        if entry["owner"] != owner:
            raise Exception(f"用户 {owner} 不是元知识 {key} 的所有者")
            
        # 更新权限
        for perm_type, users in permissions.items():
            if perm_type not in entry["permissions"]:
                entry["permissions"][perm_type] = []
            entry["permissions"][perm_type].extend([user for user in shared_with if user not in entry["permissions"][perm_type]])
            
        self.access_control[key] = entry["permissions"]
        
    def get_access_control(self, key):
        """
        获取访问控制信息
        
        Args:
            key (str): 元知识键
            
        Returns:
            dict: 访问控制信息
        """
        return self.access_control.get(key, {})
        
    def search_meta_knowledge(self, query, user):
        """
        搜索元知识（基于简化实现，实际应使用更复杂的搜索算法）
        
        Args:
            query (str): 搜索查询
            user (str): 请求用户
            
        Returns:
            list: 匹配的元知识键列表
        """
        results = []
        
        for key, entry in self.meta_knowledge_base.items():
            # 检查读权限
            if "read" in entry["permissions"] and user in entry["permissions"]["read"]:
                # 解密数据以进行搜索
                try:
                    decrypted_data = self.cipher.decrypt(entry["data"]).decode()
                    if query in decrypted_data:
                        results.append(key)
                except:
                    # 解密失败，跳过
                    pass
                    
        return results
    
    def _protect_data_privacy(self, data: dict, privacy_level: str) -> dict:
        """
        根据隐私级别保护数据
        
        Args:
            data (dict): 原始数据
            privacy_level (str): 隐私级别 (public, internal, confidential)
            
        Returns:
            dict: 保护后的数据
        """
        if privacy_level == 'public':
            # 公开数据无需保护
            return data
        elif privacy_level == 'internal':
            # 内部数据，移除敏感字段
            protected_data = data.copy()
            sensitive_fields = ['password', 'secret', 'key', 'token']
            for field in sensitive_fields:
                if field in protected_data:
                    del protected_data[field]
            return protected_data
        elif privacy_level == 'confidential':
            # 机密数据，只保留元数据
            return {
                'type': data.get('type', 'unknown'),
                'size': len(str(data)),
                'created_at': data.get('created_at', datetime.now().isoformat())
            }
        else:
            return data
    
    def _apply_privacy_filters(self, data: dict, privacy_level: str) -> dict:
        """
        应用隐私过滤器
        
        Args:
            data (dict): 数据
            privacy_level (str): 隐私级别
            
        Returns:
            dict: 过滤后的数据
        """
        # 这里可以实现更复杂的隐私过滤逻辑
        return data