import InformationSystem
import MemoryProvider
import OllamaModel
import RandomSystem
import Reminder

"""
综合实现
管理运行流程
从启动到结束

"""

class LIghtas:
    def __init__(self,model:OllamaModel,info:InformationSystem,memo:MemoryProvider,rand:RandomSystem,reminder:Reminder): # 本目录下的类,截取前4个字母,model默认为ollamamodel
        self.model=model
        self.info=info
        self.memo=memo
        self.rand=rand
        self.reminder=reminder
    def boot(self):
        Initprompt=self.rand.GetInitprompt()    # 获得一条随机启动提示词
        memory=self.memo.GetMemoty()
            # 启动时 第一句提示词是 {initprompt} + {memory} + {system prompt}  系统提示词作为全局变量定义在__init__.py
        if memory == None:
            BootResponsed = self.model.generate_completion(Initprompt) # 默认传入系统提示词
            return BootResponsed
        messages=self.reminder.GetMessages(memory,Initprompt) # 格式[{}]    
        BootResponsed= self.model.chat(messages)        # 启动响应
        return BootResponsed
    
    
    
