import datetime
import RandomSystem
import asyncio  # 异步编程

"""
    它的作用主要是构建提示词
    单个回复是 prompt(没有聊天记录,能传入system系统提示词)
    上下文对话是chat ,需要reminder构建messages  格式如下[ {'role':"xxxx",'content':"xxxx"},{...,...} ]

"""

class ReminderSystem:
    def __init__(self):
        self.messages = []

    def get_init_prompt(self):
        prompts = ["启动提示词1", "启动提示词2", "启动提示词3"]
        return random.choice(prompts)

    def get_messages(self, init_prompt):
        self.messages.append({'role': 'system', 'content': init_prompt})
        return self.messages

    def get_prompt(self, result):
        return f"基于结果生成的新提示词: {result}"

    def judge_again(self, response):
        return f"重新判断的结果: {response}"

    def get_summary(self):
        if random.random() < 0.1:  # 10% 概率触发总结
            return "这是一个总结。"
        return None

    def get_choice(self):
        choices = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
        return random.choice(choices)