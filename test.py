import datetime
import random
import subprocess
import ollama
import asyncio

# 全局变量
EmbeddingModel = "nomic-embed-text:latest"
SystemPrompt = ""
host = '127.0.0.1'
port = '11434'

# 随机系统
class RandomSystem:
    def __init__(self):
        pass

    def get_choice(self, choices):
        return random.choice(choices)

    def insert_random_info(self, text):
        current_time = datetime.datetime.now().strftime("%H:%M")
        info = f"{text} {random.choice(['当前时间为:', '现在是:', '时间:'])} {current_time}"
        return info

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

# 信息系统
class InformationSystem:
    def __init__(self):
        pass

    def search(self, query):
        # 模拟搜索请求
        return f"Search results for query: {query}"

# 提醒系统
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

# Lightas 系统核心类
class Lightas:
    def __init__(self, ollama: ollama, info: InformationSystem, memo: MemoryProvider, rand: RandomSystem, reminder: ReminderSystem):
        self.ollama = ollama
        self.model = ollama.list()
        self.info = info
        self.memo = memo
        self.rand = rand
        self.reminder = reminder
        self.choices = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
        self.prompt = ""
        self.response = ""
        self.embedding = ""

    def boot(self):
        init_prompt = self.reminder.get_init_prompt()  # 获得一条随机启动提示词
        memory = self.memo.get_memory()
        if memory is None:
            boot_response = self.model.generate_completion(init_prompt)  # 默认传入系统提示词
            self.main(boot_response)
            return boot_response
        messages = self.reminder.get_messages(init_prompt)  # 格式[{}]    
        boot_response = self.model.chat(messages)  # 启动响应
        self.main(boot_response)
        return boot_response
    
    def main(self, response):
        summary = self.reminder.get_summary()  # 随机概率返回总结
        if summary is not None:
            response = f"{summary}, {response}"
        choice = self.judge(response)
        if choice not in self.choices:
            self.reminder.remind()
            choice = self.reminder.get_choice()
        result = self.run(choice)
        prompt = self.reminder.get_prompt(result)  # 由程序运行结果生成新的提示词
        message = self.reminder.get_messages(prompt)
        return self.ollama.chat(message)

    def judge(self, response):
        judge_prompt = f"现在请你充当决策判断师,请你判断:{response} || Q: 请问以上决策选择的是哪一个选项?(仅回答选项)"
        judge_result = self.model.generate_completion(judge_prompt)
        if judge_result not in self.choices:
            judge_result = self.reminder.judge_again(judge_result)
        return judge_result  # ["A", "B",.........."Z"]

    def run(self, choice):
        try:
            result = subprocess.run(["python", f"../lib/{choice}.py"], capture_output=True, text=True, check=True)
            output = result.stdout
            return output
        except subprocess.CalledProcessError as e:
            return f"发生错误，错误类型: {type(e).__name__}，错误信息: {str(e)}"

# 使用示例
if __name__ == "__main__":
    # 创建必要的模块实例
    gemma = ollama()
    ollama_instance = ollama.Ollama()  # 替换为实际的 Ollama 实例
    info_system = InformationSystem()
    memory_provider = MemoryProvider()
    random_system = RandomSystem()
    reminder_system = ReminderSystem()

    # 创建 Lightas 对象
    lightas = Lightas(ollama_instance, info_system, memory_provider, random_system, reminder_system)

    # 启动系统
    boot_response = lightas.boot()
    print("Boot Response:", boot_response)
