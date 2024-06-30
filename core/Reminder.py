import datetime
import RandomSystem


"""
    它的作用主要是构建提示词
    单个回复是 prompt(没有聊天记录,能传入system系统提示词)
    上下文对话是chat ,需要reminder构建messages  格式如下[ {'role':"xxxx",'content':"xxxx"},{...,...} ]

"""

class ReminderSystem:
    def __init__(self) :
        self.time= datetime.datetime.now()  #系统当前时间
        self.environment="..DATA/MY_environment"#当前操作系统的环境 (可以通过neofetch查看)
        self.memory= "../DATA/MY_memory"
        self.plan="../DATA/MY_plan" 
        self.note="../DATA/MY_note" # 一个临时的笔记本


    def GetInitprompt(self):  # 获得初始提示词 
        InitPrompt = "你现在处于一个虚拟操作系统中,我将向你提供" # 后续改为随机
        return InitPrompt


    def GetMessages(self,prompt): # 获得[{ "role": "user", "content": "why is the sky blue?" },{更多记录...}]格式的message
        messages = []
        message = {"role": "user", "content": prompt} # 将消息数据包装成字典，并添加到messages列表中
        messages.append(message)
        # 返回消息列表
        return messages