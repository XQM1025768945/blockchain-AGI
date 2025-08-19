"""
自我拓展机制

实现能力评估、资源分配和动态优化
"""

import os
import psutil
import shutil
import sys
import json
import platform
import logging
from datetime import datetime
from typing import Dict, Any

# 添加项目根目录到sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 导入统一日志配置
import logging_config

# 设置日志配置
logging_config.setup_logging()
logger = logging_config.get_logger('self_expansion')


class SelfExpansion:
    def __init__(self, model_path):
        """
        初始化自我拓展机制
        
        Args:
            model_path (str): 模型文件路径
        """
        self.model_path = model_path
        self.expansion_log = []
        self.performance_history = []  # 存储性能历史数据
        self.capabilities = {
            "compute": 0.0,  # 计算能力
            "memory": 0.0,   # 内存能力
            "storage": 0.0,  # 存储能力
            "network": 0.0   # 网络能力
        }
        
        # 初始化日志记录
        self.logger = logging_config.get_logger('self_expansion')
        
    def assess_capabilities(self):
        """
        评估终端能力
        """
        self.logger.info("开始评估终端能力...")
        
        # 评估计算能力（简化实现，实际应进行更复杂的计算测试）
        cpu_percent = psutil.cpu_percent(interval=1)
        self.capabilities["compute"] = 100 - cpu_percent  # 简化表示
        
        # 评估内存能力
        memory = psutil.virtual_memory()
        self.capabilities["memory"] = memory.available / (1024**3)  # GB
        
        # 评估存储能力
        if os.name == 'nt':  # Windows系统
            disk = shutil.disk_usage("C:\\")
        else:  # Unix/Linux系统
            disk = shutil.disk_usage("/")
        self.capabilities["storage"] = disk.free / (1024**3)  # GB
        
        # 评估网络能力（简化实现）
        # 实际应测试网络带宽
        self.capabilities["network"] = 100.0  # Mbps，简化表示
        
        # 记录评估结果到历史数据
        self.performance_history.append({
            "timestamp": datetime.now().isoformat(),
            "capabilities": self.capabilities.copy()
        })
        
        self.logger.info(f"能力评估结果已记录到历史数据")
        
        # 保持历史数据在合理范围内
        if len(self.performance_history) > 100:
            self.performance_history = self.performance_history[-100:]
            self.logger.info("历史数据已截取到最近100条记录")
        
        # 记录日志
        self.expansion_log.append({
            "action": "assess_capabilities",
            "capabilities": self.capabilities.copy(),
            "timestamp": datetime.now(),
            "status": "completed"
        })
        
        self.logger.info(f"能力评估完成: {self.capabilities}")
        
    def allocate_resources(self, task_requirements):
        """
        根据任务需求分配资源
        
        Args:
            task_requirements (dict): 任务需求
            
        Returns:
            dict: 资源分配方案
        """
        self.logger.info("开始资源分配...")
        
        allocation = {}
        
        # 计算资源分配
        if "compute" in task_requirements:
            required_compute = task_requirements["compute"]
            available_compute = self.capabilities["compute"]
            allocation["compute"] = min(required_compute, available_compute)
            
        # 内存资源分配
        if "memory" in task_requirements:
            required_memory = task_requirements["memory"]
            available_memory = self.capabilities["memory"]
            allocation["memory"] = min(required_memory, available_memory)
            
        # 存储资源分配
        if "storage" in task_requirements:
            required_storage = task_requirements["storage"]
            available_storage = self.capabilities["storage"]
            allocation["storage"] = min(required_storage, available_storage)
            
        # 网络资源分配
        if "network" in task_requirements:
            required_network = task_requirements["network"]
            available_network = self.capabilities["network"]
            allocation["network"] = min(required_network, available_network)
            
        # 使用智能算法优化分配计划
        optimized_plan = self._optimize_allocation(allocation, task_requirements)
        self.logger.info(f"资源分配计划已优化")
        
        # 记录日志
        self.expansion_log.append({
            "action": "allocate_resources",
            "task_requirements": task_requirements,
            "allocation": optimized_plan,
            "timestamp": datetime.now(),
            "status": "completed"
        })
        
        self.logger.info(f"资源分配完成: {optimized_plan}")
        return optimized_plan
        
    def dynamic_optimization(self, performance_feedback):
        """
        根据性能反馈进行动态优化
        
        Args:
            performance_feedback (dict): 性能反馈
        """
        self.logger.info("开始动态优化...")
        
        # 根据性能反馈调整能力评估
        if "compute_utilization" in performance_feedback:
            # 如果CPU利用率高，可能需要降低计算能力评估
            if performance_feedback["compute_utilization"] > 80:
                self.capabilities["compute"] *= 0.9
            elif performance_feedback["compute_utilization"] < 20:
                self.capabilities["compute"] *= 1.1
                
        if "memory_usage" in performance_feedback:
            # 如果内存使用率高，降低内存能力评估
            if performance_feedback["memory_usage"] > 80:
                self.capabilities["memory"] *= 0.9
            elif performance_feedback["memory_usage"] < 20:
                self.capabilities["memory"] *= 1.1
                
        # 生成优化计划
        optimization_plan = self._generate_optimization_plan(performance_feedback)
        self.logger.info(f"动态优化计划已生成")
        
        # 记录优化结果
        self.expansion_log.append({
            "event": "optimization",
            "timestamp": datetime.now().isoformat(),
            "plan": optimization_plan
        })
        
        # 记录日志
        self.expansion_log.append({
            "action": "dynamic_optimization",
            "performance_feedback": performance_feedback,
            "updated_capabilities": self.capabilities.copy(),
            "timestamp": datetime.now(),
            "status": "completed"
        })
        
        self.logger.info(f"动态优化完成，更新后的能力: {self.capabilities}")
        
    def expand_capabilities(self, expansion_plan):
        """
        根据拓展计划扩展能力
        
        Args:
            expansion_plan (dict): 拓展计划
        """
        self.logger.info("开始能力拓展...")
        
        # 根据拓展计划更新能力
        for capability, improvement in expansion_plan.items():
            if capability in self.capabilities:
                old_value = self.capabilities[capability]
                self.capabilities[capability] *= (1 + improvement / 100)
                self.logger.info(f"能力 {capability} 已更新: {old_value} -> {self.capabilities[capability]}")
                
        # 记录日志
        self.expansion_log.append({
            "action": "expand_capabilities",
            "expansion_plan": expansion_plan,
            "updated_capabilities": self.capabilities.copy(),
            "timestamp": datetime.now(),
            "status": "completed"
        })
        
        self.logger.info(f"能力拓展完成，更新后的能力: {self.capabilities}")
    
    def get_capabilities(self):
        """
        获取当前能力信息
        
        Returns:
            dict: 当前能力信息
        """
        return self.capabilities.copy()
        
    def get_capabilities(self):
        """
        获取当前能力评估
        
        Returns:
            dict: 能力评估
        """
        return self.capabilities.copy()
        
    def _optimize_allocation(self, allocation_plan: dict, task_requirements: dict) -> dict:
        """
        优化资源分配计划
        
        Args:
            allocation_plan (dict): 初始分配计划
            task_requirements (dict): 任务需求
            
        Returns:
            dict: 优化后的分配计划
        """
        # 基于历史性能数据和任务需求优化分配
        # 这里简化实现，实际应使用更复杂的算法
        
        # 如果有历史数据，根据历史性能调整分配
        if self.performance_history:
            # 计算平均性能
            avg_cpu = sum([entry["capabilities"]["compute"] for entry in self.performance_history]) / len(self.performance_history)
            avg_memory = sum([entry["capabilities"]["memory"] for entry in self.performance_history]) / len(self.performance_history)
            
            # 根据历史性能调整分配
            if avg_cpu > 80:  # CPU使用率过高
                allocation_plan["compute"] = min(allocation_plan["compute"] * 1.2, 100)
            if avg_memory > 80:  # 内存使用率过高
                allocation_plan["memory"] = min(allocation_plan["memory"] * 1.2, 100)
                
        return allocation_plan
        
    def _generate_optimization_plan(self, performance_feedback: dict) -> dict:
        """
        根据性能反馈生成优化计划
        
        Args:
            performance_feedback (dict): 性能反馈
            
        Returns:
            dict: 优化计划
        """
        plan = {
            "timestamp": datetime.now().isoformat(),
            "actions": []
        }
        
        # 根据CPU利用率生成优化建议
        if "compute_utilization" in performance_feedback:
            cpu_util = performance_feedback["compute_utilization"]
            if cpu_util > 80:
                plan["actions"].append({
                    "type": "reduce_compute_load",
                    "reason": f"CPU利用率过高 ({cpu_util}%)",
                    "suggestion": "考虑任务分流或增加计算资源"
                })
            elif cpu_util < 20:
                plan["actions"].append({
                    "type": "increase_compute_load",
                    "reason": f"CPU利用率过低 ({cpu_util}%)",
                    "suggestion": "可以接受更多计算任务以提高资源利用率"
                })
                
        # 根据内存使用率生成优化建议
        if "memory_usage" in performance_feedback:
            memory_usage = performance_feedback["memory_usage"]
            if memory_usage > 80:
                plan["actions"].append({
                    "type": "reduce_memory_usage",
                    "reason": f"内存使用率过高 ({memory_usage}%)",
                    "suggestion": "考虑内存优化或增加内存资源"
                })
            elif memory_usage < 20:
                plan["actions"].append({
                    "type": "increase_memory_usage",
                    "reason": f"内存使用率过低 ({memory_usage}%)",
                    "suggestion": "可以接受更多内存密集型任务以提高资源利用率"
                })
                
        return plan
        
    def predict_capabilities(self, time_horizon: int = 3600) -> dict:
        """
        预测未来能力
        
        Args:
            time_horizon (int): 预测时间范围（秒）
            
        Returns:
            dict: 预测的能力信息
        """
        if not self.performance_history:
            # 没有历史数据，返回当前评估
            return self.assess_capabilities()
            
        # 简化的线性预测模型
        # 实际应使用更复杂的预测算法（如时间序列分析）
        recent_data = self.performance_history[-10:]  # 使用最近10个数据点
        
        # 计算趋势
        if len(recent_data) < 2:
            return self.assess_capabilities()
            
        # 简单线性回归预测
        timestamps = [datetime.fromisoformat(entry["timestamp"]).timestamp() for entry in recent_data]
        cpu_values = [entry["capabilities"]["compute"] for entry in recent_data]
        memory_values = [entry["capabilities"]["memory"] for entry in recent_data]
        
        # 计算斜率
        n = len(timestamps)
        sum_x = sum(timestamps)
        sum_y_cpu = sum(cpu_values)
        sum_y_memory = sum(memory_values)
        sum_xy_cpu = sum([timestamps[i] * cpu_values[i] for i in range(n)])
        sum_xy_memory = sum([timestamps[i] * memory_values[i] for i in range(n)])
        sum_x2 = sum([x * x for x in timestamps])
        
        # 避免除零错误
        if n * sum_x2 - sum_x * sum_x == 0:
            return self.assess_capabilities()
            
        slope_cpu = (n * sum_xy_cpu - sum_x * sum_y_cpu) / (n * sum_x2 - sum_x * sum_x)
        slope_memory = (n * sum_xy_memory - sum_x * sum_y_memory) / (n * sum_x2 - sum_x * sum_x)
        
        # 预测未来值
        current_time = datetime.now().timestamp()
        future_time = current_time + time_horizon
        
        predicted_cpu = cpu_values[-1] + slope_cpu * (future_time - timestamps[-1])
        predicted_memory = memory_values[-1] + slope_memory * (future_time - timestamps[-1])
        
        # 限制预测值在合理范围内
        predicted_cpu = max(0, min(100, predicted_cpu))
        predicted_memory = max(0, min(100, predicted_memory))
        
        return {
            "compute": predicted_cpu,
            "memory": predicted_memory,
            "storage": self.assess_capabilities()["storage"],  # 存储暂时不预测
            "network": self.assess_capabilities()["network"]  # 网络暂时不预测
        }
        
    def get_expansion_log(self):
        """
        获取拓展日志
        
        Returns:
            list: 拓展日志
        """
        return self.expansion_log