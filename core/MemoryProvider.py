 
"""
    主要提供对话记录等各种记录
    包含数据库存储与调用

"""
# 记忆提供者
class MemoryProvider:
    def __init__(self):
        self.memory = []

    def add_memory(self, text):
        self.memory.append(text)

    def get_memory(self):
        if self.memory:
            return random.choice(self.memory)
        return None