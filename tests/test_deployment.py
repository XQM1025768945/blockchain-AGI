import unittest
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from deployment.global_brain_deployment import GlobalBrainDeployment

class TestGlobalBrainDeployment(unittest.TestCase):
    """
    全球AI脑部署机制测试类
    """
    
    def setUp(self):
        """
        测试前准备
        """
        self.deployment = GlobalBrainDeployment(
            model_repo_url="http://test.repo/models",
            model_path="./test_model.pt"
        )
    
    def test_initialization(self):
        """
        测试初始化
        """
        self.assertIsInstance(self.deployment, GlobalBrainDeployment)
        self.assertEqual(self.deployment.model_repo_url, "http://test.repo/models")
        self.assertEqual(self.deployment.model_path, "./test_model.pt")
    
    def test_deploy_globally(self):
        """
        测试全球部署功能
        """
        # 模拟部署过程
        self.deployment.deploy_globally(network_range="192.168.1", port=8888)
        
        # 验证部署状态
        status = self.deployment.get_deployment_status()
        # 检查状态是否为字典且包含必要的键
        self.assertIsInstance(status, dict)
        self.assertIn('deployment_log', status)
        self.assertIn('nodes_deployed', status)
    
    def test_activate_globally(self):
        """
        测试全球激活功能
        """
        # 先部署
        self.deployment.deploy_globally(network_range="192.168.1", port=8888)
        
        # 激活
        self.deployment.activate_globally()
        
        # 验证激活状态
        status = self.deployment.get_deployment_status()
        # 检查状态是否为字典且包含必要的键
        self.assertIsInstance(status, dict)
        self.assertIn('is_active', status)
        self.assertTrue(status['is_active'])
    
    def test_expand_globally(self):
        """
        测试全球能力拓展功能
        """
        # 先部署和激活
        self.deployment.deploy_globally(network_range="192.168.1", port=8888)
        self.deployment.activate_globally()
        
        # 拓展能力
        expansion_plan = {
            "compute": 10.0,
            "memory": 20.0
        }
        self.deployment.expand_globally(expansion_plan)
        
        # 验证拓展状态
        status = self.deployment.get_deployment_status()
        # 检查状态是否为字典且包含必要的键
        self.assertIsInstance(status, dict)

if __name__ == '__main__':
    unittest.main()