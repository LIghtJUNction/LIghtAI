 
"""
    说白了就是给AI洗脑用的
    它的作用主要是构建提示词
    单个回复是 prompt(没有聊天记录,能传入system系统提示词)
    上下文对话是chat ,需要reminder构建messages  格式如下[ {'role':"xxxx",'content':"xxxx"},{...,...} ]
    

"""

class ReminderSystem:
    def __init__(self) :
        self