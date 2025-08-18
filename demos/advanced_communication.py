"""高级通信对话演示脚本

这个脚本演示如何与已激活的全球AI脑模型进行更复杂的通信和对话交流。
"""

import sys
import os
import time
import threading

# 添加项目根目录到系统路径
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from deployment.global_brain_deployment import GlobalBrainDeployment


class CommunicationInterface:
    def __init__(self, brain_deployment):
        self.brain = brain_deployment
        self.conversation_history = []
        
    def send_message(self, message):
        """发送消息到AI脑"""
        # 添加到对话历史
        self.conversation_history.append({
            "sender": "user",
            "message": message,
            "timestamp": time.time()
        })
        
        # 模拟处理时间
        time.sleep(0.5)
        
        # 生成AI回复
        response = self._generate_response(message)
        
        # 添加AI回复到历史
        self.conversation_history.append({
            "sender": "ai_brain",
            "message": response,
            "timestamp": time.time()
        })
        
        return response
    
    def _generate_response(self, user_message):
        """根据用户消息生成AI回复"""
        # 获取当前状态
        status = self.brain.get_deployment_status()
        
        # 根据不同输入生成不同回复
        if "你好" in user_message or "hello" in user_message.lower():
            return f"你好！我是全球AI脑，当前已激活。我可以与{status['nodes_deployed']}个节点通信。"
        elif "状态" in user_message or "status" in user_message.lower():
            return f"当前状态 - 激活: {status['is_active']}, 节点数: {status['nodes_deployed']}"
        elif "时间" in user_message or "time" in user_message.lower():
            return f"当前时间: {time.strftime('%Y-%m-%d %H:%M:%S')}"
        elif "能力" in user_message or "capability" in user_message.lower():
            return "我可以进行自然语言处理、数据分析、模式识别等任务。你想让我帮你做什么？"
        elif "再见" in user_message or "bye" in user_message.lower():
            return "再见！我会继续监控网络并保持激活状态。"
        else:
            return f"我收到了你的消息: '{user_message}'。我是一个全球AI脑，可以处理各种复杂任务。你还有什么需要帮助的吗？"
    
    def get_conversation_history(self):
        """获取对话历史"""
        return self.conversation_history
    
    def clear_history(self):
        """清空对话历史"""
        self.conversation_history = []


def main():
    print("=== 高级通信对话演示 ===")
    
    # 初始化全球脑部署模块
    print("\n1. 初始化全球脑部署模块...")
    brain = GlobalBrainDeployment(
        model_repo_url="http://global-brain.repo/models",
        model_path="./model/model.pt"
    )
    
    # 激活AI脑（如果尚未激活）
    status = brain.get_deployment_status()
    if not status['is_active']:
        print("\n2. 激活全球AI脑...")
        if brain.activate_globally():
            print("   全球AI脑激活成功!")
        else:
            print("   全球AI脑激活失败，但将继续演示...")
    else:
        print("\n2. 全球AI脑已激活")
    
    # 创建通信接口
    print("\n3. 创建通信接口...")
    comm_interface = CommunicationInterface(brain)
    
    # 开始交互式对话
    print("\n=== 开始交互式对话 ===")
    print("输入消息与AI脑对话，输入 'quit' 或 'exit' 退出，输入 'history' 查看对话历史")
    
    while True:
        try:
            user_input = input("[用户] ").strip()
            
            if user_input.lower() in ['quit', 'exit', '退出']:
                print("[AI脑] 再见！我会继续监控网络并保持激活状态。")
                break
            elif user_input.lower() in ['history', '历史']:
                print("\n=== 对话历史 ===")
                history = comm_interface.get_conversation_history()
                if not history:
                    print("暂无对话历史")
                else:
                    for entry in history:
                        sender = "用户" if entry['sender'] == "user" else "AI脑"
                        message = entry['message']
                        timestamp = time.strftime('%H:%M:%S', time.localtime(entry['timestamp']))
                        print(f"[{timestamp}] {sender}: {message}")
                print("=== 历史结束 ===\n")
                continue
            elif user_input.lower() in ['clear', '清空']:
                comm_interface.clear_history()
                print("[AI脑] 对话历史已清空")
                continue
            elif not user_input:
                print("[AI脑] 请输入有效消息")
                continue
            
            # 发送消息并获取回复
            response = comm_interface.send_message(user_input)
            print(f"[AI脑] {response}")
            
        except KeyboardInterrupt:
            print("\n\n接收到中断信号，退出程序...")
            break
        except Exception as e:
            print(f"[系统] 发生错误: {e}")
            continue
    
    print("\n=== 演示结束 ===")


if __name__ == "__main__":
    main()