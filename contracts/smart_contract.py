"""
智能合约模块

实现区块智能功能，包括数据分析、异常检测、预测模型、自动化决策和安全审计
"""

import hashlib
import json
import re
from datetime import datetime


class SmartContract:
    def __init__(self, owner, api_interface_id=None):
        """
        初始化智能合约
        
        Args:
            owner (str): 合约所有者
            api_interface_id (str): API接口ID
        """
        self.owner = owner
        self.contract_id = self._generate_contract_id()
        self.api_interface_id = api_interface_id
        self.created_at = datetime.now()
        self.functions = {}
        
    def _generate_contract_id(self):
        """
        生成合约ID
        
        Returns:
            str: 合约ID
        """
        data = f"{self.owner}{datetime.now()}".encode()
        return hashlib.sha256(data).hexdigest()
        
    def add_function(self, name, function):
        """
        添加合约函数
        
        Args:
            name (str): 函数名
            function (callable): 函数实现
        """
        self.functions[name] = function
        
    def execute_function(self, name, *args, **kwargs):
        """
        执行合约函数
        
        Args:
            name (str): 函数名
            *args: 函数参数
            **kwargs: 函数关键字参数
            
        Returns:
            any: 函数执行结果
        """
        if name not in self.functions:
            raise Exception(f"函数 {name} 不存在")
            
        return self.functions[name](*args, **kwargs)
        
    def data_analysis(self, data):
        """
        数据分析功能
        
        Args:
            data (list): 数据列表
            
        Returns:
            dict: 分析结果
        """
        if not data:
            return {"error": "数据为空"}
            
        # 简单统计分析
        result = {
            "count": len(data),
            "mean": sum(data) / len(data),
            "min": min(data),
            "max": max(data)
        }
        
        return result
        
    def anomaly_detection(self, data, threshold=2.0):
        """
        异常检测功能
        
        Args:
            data (list): 数据列表
            threshold (float): 异常阈值
            
        Returns:
            list: 异常数据点
        """
        if not data:
            return []
            
        mean = sum(data) / len(data)
        variance = sum((x - mean) ** 2 for x in data) / len(data)
        std_dev = variance ** 0.5
        
        anomalies = []
        for i, value in enumerate(data):
            if abs(value - mean) > threshold * std_dev:
                anomalies.append({"index": i, "value": value})
                
        return anomalies
        
    def predict_model(self, data, steps=1):
        """
        Simple prediction model (based on linear trend)
        
        Args:
            data (list): Historical data
            steps (int): Prediction steps
            
        Returns:
            list: Prediction results
        """
        if len(data) < 2:
            return [data[-1]] * steps if data else [0] * steps
            
        # Calculate trend
        trend = (data[-1] - data[0]) / (len(data) - 1)
        
        # Predict
        predictions = []
        last_value = data[-1]
        for i in range(steps):
            next_value = last_value + trend
            predictions.append(next_value)
            last_value = next_value
            
        return predictions
        
    def automated_decision(self, data, rules):
        """
        自动化决策功能
        
        Args:
            data (dict): 输入数据
            rules (dict): 决策规则
            
        Returns:
            dict: 决策结果
        """
        decisions = {}
        
        for key, rule in rules.items():
            if key in data:
                value = data[key]
                if "min" in rule and value < rule["min"]:
                    decisions[key] = rule["action_below"]
                elif "max" in rule and value > rule["max"]:
                    decisions[key] = rule["action_above"]
                else:
                    decisions[key] = rule.get("action_default", "no_action")
                    
        return decisions
        
    def security_audit(self, code):
        """
        安全审计功能
        
        Args:
            code (str): 合约代码
            
        Returns:
            dict: 审计结果
        """
        issues = []
        
        # 检查潜在的危险操作
        if "eval(" in code:
            issues.append("检测到潜在的eval()调用，可能存在代码注入风险")
            
        if "exec(" in code:
            issues.append("检测到潜在的exec()调用，可能存在代码注入风险")
            
        # 检查文件操作
        if "open(" in code and "write" in code:
            issues.append("检测到文件写入操作，可能存在安全风险")
            
        # 检查网络操作
        if "socket" in code or "urllib" in code or "requests" in code:
            issues.append("检测到网络操作，可能存在安全风险")
            
        # 检查系统调用
        if "os.system(" in code or "subprocess" in code:
            issues.append("检测到系统调用，可能存在安全风险")
            
        return {
            "issues_found": len(issues),
            "issues": issues,
            "is_safe": len(issues) == 0
        }
        
    def data_privacy_protection(self, data, privacy_level="basic"):
        """
        数据隐私保护功能
        
        Args:
            data (dict): 原始数据
            privacy_level (str): 隐私保护级别 (basic, enhanced, maximum)
            
        Returns:
            dict: 脱敏后的数据
        """
        protected_data = data.copy()
        
        if privacy_level == "basic":
            # 基础脱敏：隐藏部分敏感信息
            for key in protected_data:
                if "email" in key.lower():
                    email = protected_data[key]
                    if "@" in email:
                        parts = email.split("@")
                        protected_data[key] = parts[0][:2] + "***@" + parts[1]
                elif "phone" in key.lower():
                    phone = protected_data[key]
                    if len(phone) > 4:
                        protected_data[key] = phone[:-4] + "****"
                elif "id" in key.lower() or "card" in key.lower():
                    id_number = protected_data[key]
                    if len(id_number) > 8:
                        protected_data[key] = id_number[:4] + "****" + id_number[-4:]
        elif privacy_level == "enhanced":
            # 增强脱敏：使用哈希
            for key in protected_data:
                if "email" in key.lower() or "phone" in key.lower() or "id" in key.lower() or "card" in key.lower():
                    protected_data[key] = hashlib.sha256(str(protected_data[key]).encode()).hexdigest()[:16]
        elif privacy_level == "maximum":
            # 最大脱敏：完全替换
            for key in protected_data:
                if "email" in key.lower() or "phone" in key.lower() or "id" in key.lower() or "card" in key.lower():
                    protected_data[key] = "[PROTECTED]"
                    
        return protected_data
        
    def to_dict(self):
        """
        将合约转换为字典
        
        Returns:
            dict: 合约信息
        """
        result = {
            "contract_id": self.contract_id,
            "owner": self.owner,
            "created_at": self.created_at.isoformat(),
            "functions": list(self.functions.keys())
        }
        
        if self.api_interface_id:
            result["api_interface_id"] = self.api_interface_id
            
        return result
        
    def to_json(self):
        """
        将合约转换为JSON
        
        Returns:
            str: JSON字符串
        """
        return json.dumps(self.to_dict(), indent=2)