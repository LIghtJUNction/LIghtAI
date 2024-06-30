import InformationSystem
import MemoryProvider
import OllamaModel
import RandomSystem
import Reminder

import subprocess
"""
综合实现
管理运行流程
从启动到结束



    reminder.GetInitprompt(prompt)  # 获得初始化提示词
    reminder.GetMessages(prompt) # 返回带有对话记录的message
    reminder.GetPrompt(result) # 传入程序运行结果,输出带有程序运行日志的提示词
    reminder.JudgeAgain(response) # 判断有误,重新判断,返回一个新的判断结果
    reminder.GetSummary() # 概率触发 触发后本轮对话将是 总结(带系统提示词)

    reminder.GetChoice()

"""
class LIghtas:
    def __init__(self,model:OllamaModel,info:InformationSystem,memo:MemoryProvider,rand:RandomSystem,reminder:Reminder): # 本目录下的类,截取前4个字母,model默认为ollamamodel
        self.model=model
        self.info=info
        self.memo=memo
        self.rand=rand
        self.reminder=reminder
        self.choices=["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]

    def boot(self):
        Initprompt=self.reminder.GetInitprompt()    # 获得一条随机启动提示词
        memory=self.memo.GetMemoty()
            # 启动时 第一句提示词是 {initprompt} + {memory} + {system prompt}  系统提示词作为全局变量定义在__init__.py
        if memory == None:
            BootResponsed = self.model.generate_completion(Initprompt) # 默认传入系统提示词
            self.main(BootResponsed)
            return BootResponsed
        messages=self.reminder.GetMessages(Initprompt) # 格式[{}]    
        BootResponsed= self.model.chat(messages)        # 启动响应
        self.main(BootResponsed)
        return BootResponsed
    
    def main(self,response):
        summary = self.reminder.GetSummary() #  随机概率返回总结
        if summary != None:
            response = f"{summary},{response} "
        choice = self.judge(response)
        if choice not in self.choices:
            self.reminder.remind()
            choice = self.reminder.GetChoice()
        result=self.run(choice)
        prompt = self.reminder.GetPrompt(result)  # 由程序运行结果生成新的提示词
        message = self.reminder.GetMessage(prompt)
        return  self.model.chat(message)

    def judge(self,response):
        JudgePrompt = f"现在请你充当决策判断师,请你判断:{response}    || Q: 请问以上决策选择的是哪一个选项?(仅回答选项)"
        JudgeResult = self.model.generate_completion(JudgePrompt)
        if JudgeResult not in self.choices:
            self.reminder.JudgeAgain()
        return JudgeResult    # ["A","B",.........."Z"]

    def run(self,choice):
        try:
            result = subprocess.run(["python",f"../lib/{choice}.py"],capture_output=True,text=True, check=True)
            output = result.stdout
            return output
        except subprocess.CalledProcessError as e:
            return f"发生错误，错误类型: {type(e).__name__}，错误信息: {str(e)}"
        





    
