import InformationSystem
import MemoryProvider
import ollama
import RandomSystem
import Reminder
import subprocess

class Lightas:
    def __init__(self, ollama: ollama, info: InformationSystem, memo: MemoryProvider, rand: RandomSystem, reminder: Reminder):
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
        init_prompt = self.reminder.GetInitprompt()    # 获得一条随机启动提示词
        memory = self.memo.GetMemory()
        # 启动时 第一句提示词是 {initprompt} + {memory} + {system prompt}  系统提示词作为全局变量定义在__init__.py
        if memory is None:
            boot_response = self.model.generate_completion(init_prompt) # 默认传入系统提示词
            self.main(boot_response)
            return boot_response
        messages = self.reminder.GetMessages(init_prompt) # 格式[{}]    
        boot_response = self.model.chat(messages)        # 启动响应
        self.main(boot_response)
        return boot_response
    
    def main(self, response):
        summary = self.reminder.GetSummary() #  随机概率返回总结
        if summary is not None:
            response = f"{summary}, {response}"
        choice = self.judge(response)
        if choice not in self.choices:
            self.reminder.remind()
            choice = self.reminder.GetChoice()
        result = self.run(choice)
        prompt = self.reminder.GetPrompt(result)  # 由程序运行结果生成新的提示词
        message = self.reminder.GetMessages(prompt)
        return self.ollama.chat(message)

    def judge(self, response):
        judge_prompt = f"现在请你充当决策判断师,请你判断:{response} || Q: 请问以上决策选择的是哪一个选项?(仅回答选项)"
        judge_result = self.model.generate_completion(judge_prompt)
        if judge_result not in self.choices:
            judge_result = self.reminder.JudgeAgain(judge_result)
        return judge_result    # ["A","B",.........."Z"]

    def run(self, choice):
        try:
            result = subprocess.run(["python", f"../lib/{choice}.py"], capture_output=True, text=True, check=True)
            output = result.stdout
            return output
        except subprocess.CalledProcessError as e:
            return f"发生错误，错误类型: {type(e).__name__}，错误信息: {str(e)}"

# 使用示例
if __name__ == "__main__":
    # 示例数据
    data = pd.DataFrame({
        'id': [1, 2, 3],
        'text': ["This is the first document.", "This document is the second document.", "And this is the third one."]
    })

    # 创建知识库对象
    kb = VectorKnowledgeBase(data)

    # 生成文档嵌入并创建索引
    kb.generate_embeddings()
    kb.create_index()

    # 保存索引
    kb.save_index("vector_database.index")

    # 加载索引
    kb.load_index("vector_database.index")

    # 查询
    query_results = kb.query("This is a new document to query.")
    print("Query Results:", query_results)
