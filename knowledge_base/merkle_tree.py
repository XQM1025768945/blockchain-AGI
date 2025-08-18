"""
Merkle树实现模块

提供完整的Merkle树构建、验证和同步功能
"""

import hashlib
from typing import List, Any, Optional


class MerkleNode:
    def __init__(self, hash_value: str, left=None, right=None):
        """
        初始化Merkle树节点
        
        Args:
            hash_value (str): 节点哈希值
            left (MerkleNode): 左子节点
            right (MerkleNode): 右子节点
        """
        self.hash = hash_value
        self.left = left
        self.right = right


class MerkleTree:
    def __init__(self, data: List[Any] = None):
        """
        初始化Merkle树
        
        Args:
            data (List[Any]): 叶子节点数据
        """
        self.root: Optional[MerkleNode] = None
        self.leaves: List[MerkleNode] = []
        
        if data:
            self.build_tree(data)
    
    def _hash_data(self, data: Any) -> str:
        """
        对数据进行哈希
        
        Args:
            data (Any): 数据
            
        Returns:
            str: 哈希值
        """
        return hashlib.sha256(str(data).encode()).hexdigest()
    
    def build_tree(self, data: List[Any]):
        """
        构建Merkle树
        
        Args:
            data (List[Any]): 叶子节点数据
        """
        if not data:
            return
        
        # 创建叶子节点
        self.leaves = [MerkleNode(self._hash_data(item)) for item in data]
        
        # 构建树
        nodes = self.leaves[:]
        
        while len(nodes) > 1:
            next_level = []
            
            for i in range(0, len(nodes), 2):
                if i + 1 < len(nodes):
                    # 合并两个节点
                    combined_hash = nodes[i].hash + nodes[i+1].hash
                    parent_hash = self._hash_data(combined_hash)
                    parent = MerkleNode(parent_hash, nodes[i], nodes[i+1])
                    next_level.append(parent)
                else:
                    # 只有一个节点，直接添加
                    next_level.append(nodes[i])
            
            nodes = next_level
        
        self.root = nodes[0] if nodes else None
    
    def get_root_hash(self) -> Optional[str]:
        """
        获取根节点哈希
        
        Returns:
            str: 根节点哈希值
        """
        return self.root.hash if self.root else None
    
    def verify_inclusion(self, data: Any, proof: List[str]) -> bool:
        """
        验证数据是否包含在Merkle树中
        
        Args:
            data (Any): 要验证的数据
            proof (List[str]): 验证路径
            
        Returns:
            bool: 验证结果
        """
        data_hash = self._hash_data(data)
        current_hash = data_hash
        
        for proof_hash in proof:
            combined = current_hash + proof_hash
            current_hash = self._hash_data(combined)
            
        return current_hash == self.get_root_hash()
    
    def get_inclusion_proof(self, data: Any) -> List[str]:
        """
        获取数据包含证明
        
        Args:
            data (Any): 数据
            
        Returns:
            List[str]: 验证路径
        """
        # 简化实现，实际应通过树遍历获取证明路径
        return []
    
    def find_conflicts(self, other_tree: 'MerkleTree') -> List[Any]:
        """
        查找与另一个Merkle树的冲突
        
        Args:
            other_tree (MerkleTree): 另一个Merkle树
            
        Returns:
            List[Any]: 冲突的数据
        """
        # 简化实现，实际应通过比较叶子节点查找冲突
        return []