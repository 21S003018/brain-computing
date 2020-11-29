# -*- coding: utf-8 -*-
"""

"""
import os
import globalvar as gl
import json
from threading import Thread
import time

class LTM():
    def __init__(self):
        self.address = None
        self.gist = None
        self.weight = None
        self.intensity = None
        self.mood = None
        self.satisfaction = 0
        return

class SENSOR():
    def __init__(self,stm):
        self.stm = stm
        self.path = gl.get_value('environmentMessagePath')
        self.last_mtime = os.stat(self.path).st_mtime
        # print(self.last_mtime)
        Thread(target=self.run).start()
        return
    def getMessage(self):
        while self.last_mtime == os.stat(self.path).st_mtime:
            time.sleep(0.1)
        self.last_mtime = os.stat(self.path).st_mtime
        file = open(self.path, 'r')
        message = json.load(file)
        file.close()
        return message
    def run(self):
        while True:
            message = self.getMessage()
            message_v = message['vision']
            if message_v.__contains__('predator'):
                self.stm.sensor_add(label='predator')
            if message_v.__contains__('prey'):
                self.stm.sensor_add(label='prey')
            timestamp = time.time()
            # print(message)
            self.stm.process_message(message)
            if time.time() - timestamp < 1:
                time.sleep(1)
            die = False
            if gl.get_value('tired') < 0:
                die = True
            if gl.get_value('hungry') < 0:
                die = True
            if gl.get_value('thirsty') < 0:
                die = True
            if gl.get_value('pain') < 0:
                die = True
            if gl.get_value('sexy') < 0:
                die = True
            if die == True:
                break
        return

# class OPTICALSENSOR():
#     def __init__(self):
#         return
#     def collectMessage(self):
#         def content():
#             while True:
#                 '''检测环境反馈信息是否更新'''
#                 timeStamp = os.stat(gl.get_value('environmentMessagePath')).st_mtime
#                 while timeStamp == os.stat(gl.get_value('environmentMessagePath')).st_mtime:
#                     import time
#                     time.sleep(1)
#                 '''检测到环境信息文件更新，就进行信息的提取和整合'''
#                 '''shortTimeKnowledge中维护100个知识'''
#                 file = open(gl.get_value('environmentMessagePath'),'r')
#                 import json
#                 visionMessage = json.load(file)['vision']
#                 file.close()
#                 file = open(gl.get_value('shortTimeKnowledgePath'),'r')
#                 shortTimeMessage = json.load(file)
#                 file.close()
#                 newshortTimeMessage = {}
#                 i = 1
#                 for i in range(1,101):
#                     if visionMessage.__contain__(i):
#                         newshortTimeMessage[i] = visionMessage[i]
#                     else:
#                         break
#                 id = 1
#                 for x in range(i,101):
#                     if shortTimeMessage.__contains__(id):
#                         newshortTimeMessage[x] = shortTimeMessage[id]
#                         id = id + 1
#                     else:
#                         break
#                 file = open(gl.get_value('shortTimeKnowledgePath'),'w')
#                 dic = json.dumps(newshortTimeMessage)
#                 file.write(str(dic))
#                 file.close()
#         from threading import Thread
#         problem_detect_thread = Thread(target = content)
#         problem_detect_thread.setDaemon(True)
#         problem_detect_thread.start()
#         return
#
# class SOUNDSENSOR():
#     def __init__(self):
#         return
#     def collectMessage(self):
#         def content():
#             while True:
#                 '''检测文件是否更新'''
#                 timeStamp = os.stat(gl.get_value('environmentMessagePath')).st_mtime
#                 while timeStamp == os.stat(gl.get_value('environmentMessagePath')).st_mtime:
#                     import time
#                     time.sleep(1)
#                 '''检测到环境信息文件更新，就进行信息的提取和整合'''
#                 '''shortTimeKnowledge中维护100个知识'''
#                 file = open(gl.get_value('environmentMessagePath'),'r')
#                 import json
#                 visionMessage = json.load(file)['hearing']
#                 file.close()
#                 file = open(gl.get_value('shortTimeKnowledgePath'),'r')
#                 shortTimeMessage = json.load(file)
#                 file.close()
#                 newshortTimeMessage = {}
#                 i = 1
#                 for i in range(1,101):
#                     if visionMessage.__contain__(i):
#                         newshortTimeMessage[i] = visionMessage[i]
#                     else:
#                         break
#                 id = 1
#                 for x in range(i,101):
#                     if shortTimeMessage.__contains__(id):
#                         newshortTimeMessage[x] = shortTimeMessage[id]
#                         id = id + 1
#                     else:
#                         break
#                 file = open(gl.get_value('shortTimeKnowledgePath'),'w')
#                 dic = json.dumps(newshortTimeMessage)
#                 file.write(str(dic))
#                 file.close()
#         from threading import Thread
#         problem_detect_thread = Thread(target = content)
#         problem_detect_thread.setDaemon(True)
#         problem_detect_thread.start()
#         return

# I don't know what's this.
class PAIN(LTM):
    def __init__(self,initFeeling = 10):
        LTM.__init__(self)
        self.feeling = 'pain'
        gl.set_value(self.feeling,initFeeling)
    """
#    checkState方法
#    仅仅考虑这个feeling随时间因素的变化
    """
    def checkState(self):
        """
        皮肤的感官不随时间变化，暂且不做考虑
        :return:
        """
        # """
        # 暂且认为一分钟消耗0.015
        # """
        # delta = 0.015
        # def content():
        #     gl.set_value(self.feeling,gl.get_value(self.feeling) - delta)
        #     return
        # def periodicExec(func,inc = 5):
        #     import time,sched
        #     s = sched.scheduler(time.time,time.sleep)
        #     def perform(inc):
        #         s.enter(inc,0,perform,(inc,))
        #         func()
        #     s.enter(0,0,perform,(inc,))
        #     s.run()
        #     return
        # from threading import Thread
        # state_update_thread = Thread(target = periodicExec,args = (content,))
        # state_update_thread.setDaemon(True)
        # state_update_thread.start()
        return
    """
#    getNeedIntensity方法
#    根据自身的状态返回需求强度
#    返回值是一个元组
    """
    def getNeedIntensity(self):
        need = 10 / gl.get_value(self.feeling)
        return (need,self.feeling)

# 生理需求
class SLEEP(LTM):
    def __init__(self, initFeeling=10):
        LTM.__init__(self)
        self.feeling = "tired"
        gl.set_value(self.feeling, initFeeling)
        return

    def cal_weight(self):
        return 10 - gl.get_value(self.feeling)

    """
#    checkState方法
#    仅仅考虑这个feeling随时间因素的变化
    """

    def checkState(self):
        """
        暂且认为一分钟消耗0.015
        """
        delta = 0.015

        def content():
            gl.set_value(self.feeling, gl.get_value(self.feeling) - delta)
            return

        def periodicExec(func, inc=5):
            import time, sched
            s = sched.scheduler(time.time, time.sleep)

            def perform(inc):
                s.enter(inc, 0, perform, (inc,))
                func()

            s.enter(0, 0, perform, (inc,))
            s.run()
            return

        from threading import Thread
        state_update_thread = Thread(target=periodicExec, args=(content,))
        state_update_thread.setDaemon(True)
        state_update_thread.start()
        return

class ENERGY(LTM):
    def __init__(self,initFeeling = 10):
        LTM.__init__(self)
        self.feeling = 'hungry'
        gl.set_value(self.feeling,initFeeling)

    def cal_weight(self):
        return 10 - gl.get_value(self.feeling)

    """
#    checkState方法
#    仅仅考虑这个feeling随时间因素的变化
    """
    def checkState(self):
        """
        暂且认为一分钟消耗0.015
        """
        delta = 0.1
        def content():
            gl.set_value(self.feeling,gl.get_value(self.feeling) - delta)
            return
        def periodicExec(func,inc = 5):
            import time,sched
            s = sched.scheduler(time.time,time.sleep)
            def perform(inc):
                s.enter(inc,0,perform,(inc,))
                func()
            s.enter(0,0,perform,(inc,))
            s.run()
            return
        from threading import Thread
        state_update_thread = Thread(target = periodicExec,args = (content,))
        state_update_thread.setDaemon(True)
        state_update_thread.start()
        return
    """
#    getNeedIntensity方法
#    根据自身的状态返回需求强度
#    返回值是一个元组
    """
    def getNeedIntensity(self):
        needOfHungry = 10 / gl.get_value(self.feeling)
        return (needOfHungry,self.feeling)

class WATER(LTM):
    def __init__(self,initFeeling = 10):
        LTM.__init__(self)
        self.feeling = 'thirsty'
        gl.set_value(self.feeling,initFeeling)

    def cal_weight(self):
        return 10 - gl.get_value(self.feeling)

    """
#    checkState方法
#    仅仅考虑这个feeling随时间因素的变化
    """
    def checkState(self):
        """
        暂且认为一分钟消耗0.015
        """
        delta = 0.015
        def content():
            gl.set_value(self.feeling,gl.get_value(self.feeling) - delta)
            return
        def periodicExec(func,inc = 5):
            import time,sched
            s = sched.scheduler(time.time,time.sleep)
            def perform(inc):
                s.enter(inc,0,perform,(inc,))
                func()
            s.enter(0,0,perform,(inc,))
            s.run()
            return
        from threading import Thread
        state_update_thread = Thread(target = periodicExec,args = (content,))
        state_update_thread.setDaemon(True)
        state_update_thread.start()
        return
    """
#    getNeedIntensity方法
#    根据自身的状态返回需求强度
#    返回值是一个元组
    """
    def getNeedIntensity(self):
        need = 10 / gl.get_value(self.feeling)
        return (need,self.feeling)

class BREED(LTM):
    def __init__(self,initFeeling = 10):
        LTM.__init__(self)
        self.feeling = 'sexy'
        gl.set_value(self.feeling,initFeeling)

    def cal_weight(self):
        return 10 - gl.get_value(self.feeling)

    """
#    checkState方法
#    仅仅考虑这个feeling随时间因素的变化
    """
    def checkState(self):
        """
        暂且认为一分钟消耗0.015
        """
        delta = 0.015
        def content():
            gl.set_value(self.feeling,gl.get_value(self.feeling) - delta)
            return
        def periodicExec(func,inc = 5):
            import time,sched
            s = sched.scheduler(time.time,time.sleep)
            def perform(inc):
                s.enter(inc,0,perform,(inc,))
                func()
            s.enter(0,0,perform,(inc,))
            s.run()
            return
        from threading import Thread
        state_update_thread = Thread(target = periodicExec,args = (content,))
        state_update_thread.setDaemon(True)
        state_update_thread.start()
        return
    """
#    getNeedIntensity方法
#    根据自身的状态返回需求强度
#    返回值是一个元组
    """
    def getNeedIntensity(self):
        need = 10 / gl.get_value(self.feeling)
        return (need,self.feeling)

# 安全需求
class PERSONAL_SAFETY(LTM):
    def __init__(self):
        LTM.__init__(self)
        gl.set_value('personal safety',10)
        self.feeling = 'personal safety'
        # self.lowlevel_ltms = lowlevelltms
        self.sons = ['tired','hungry','thirsty']
        # for ltm in self.lowlevel_ltms:
        #     if self.sons.__contains__(ltm.feeling):
        #         self.sons.remove(ltm.feeling)
        #         self.sons.append(ltm)
        self.alpha = 0 # 应该是负数
        self.beta = 0
        self.gamma = 0
        self.delta = 0
        return
    # def __init__(self,lowlevelltms):
    #     LTM.__init__(self)
    #     self.feeling = 'personal safety'
    #     self.lowlevel_ltms = lowlevelltms
    #     self.sons = ['tired','hungry','thirsty']
    #     for ltm in self.lowlevel_ltms:
    #         if self.sons.__contains__(ltm.feeling):
    #             self.sons.remove(ltm.feeling)
    #             self.sons.append(ltm)
    #     self.alpha = 0 # 应该是负数
    #     self.beta = 0
    #     self.gamma = 0
    #     self.delta = 0
    #     return

    def cal_weight(self):
        ans = self.delta
        ans += self.alpha * (self.satisfaction)
        for ltm in self.lowlevel_ltms:
            ans += self.beta * sum([tmp.satisfaction for tmp in self.sons])
        for ltm in self.sons:
            ans += self.gamma * sum([tmp.satisfaction for tmp in self.sons])
        return ans

class PROPERTY_SAFETY(LTM):
    def __init__(self,lowlevelltms):
        LTM.__init__(self)
        self.feeling = 'property safety'
        self.lowlevel_ltms = lowlevelltms
        self.sons = ['hungry','thirsty']
        for ltm in self.lowlevel_ltms:
            if self.sons.__contains__(ltm.feeling):
                self.sons.remove(ltm.feeling)
                self.sons.append(ltm)
        self.alpha = 0 # 应该是负数
        self.beta = 0
        self.gamma = 0
        self.delta = 0
        return

    def cal_weight(self):
        ans = self.delta
        ans += self.alpha * (self.satisfaction)
        for ltm in self.lowlevel_ltms:
            ans += self.beta * sum([tmp.satisfaction for tmp in self.sons])
        for ltm in self.sons:
            ans += self.gamma * sum([tmp.satisfaction for tmp in self.sons])
        return ans

# 社交需求
class FAMILY_AFFECTION(LTM):
    def __init__(self,lowlevelltms):
        LTM.__init__(self)
        self.feeling = 'family affection'
        self.lowlevel_ltms = lowlevelltms
        self.sons = ['personal safety','property safety']
        for ltm in self.lowlevel_ltms:
            if self.sons.__contains__(ltm.feeling):
                self.sons.remove(ltm.feeling)
                self.sons.append(ltm)
        self.alpha = 0 # 应该是负数
        self.beta = 0
        self.gamma = 0
        self.delta = 0
        return

    def cal_weight(self):
        ans = self.delta
        ans += self.alpha * (self.satisfaction)
        for ltm in self.lowlevel_ltms:
            ans += self.beta * sum([tmp.satisfaction for tmp in self.sons])
        for ltm in self.sons:
            ans += self.gamma * sum([tmp.satisfaction for tmp in self.sons])
        return ans
class FRIENDSHIP(LTM):
    def __init__(self):
        LTM.__init__(self)
        gl.set_value('friendship', 10)
        self.feeling = 'friendship'
        # self.lowlevel_ltms = lowlevelltms
        self.sons = ['personal safety','property safety']
        # for ltm in self.lowlevel_ltms:
        #     if self.sons.__contains__(ltm.feeling):
        #         self.sons.remove(ltm.feeling)
        #         self.sons.append(ltm)
        self.alpha = 0 # 应该是负数
        self.beta = 0
        self.gamma = 0
        self.delta = 0
        return
    # def __init__(self,lowlevelltms):
    #     LTM.__init__(self)
    #     self.feeling = 'friendship'
    #     self.lowlevel_ltms = lowlevelltms
    #     self.sons = ['personal safety','property safety']
    #     for ltm in self.lowlevel_ltms:
    #         if self.sons.__contains__(ltm.feeling):
    #             self.sons.remove(ltm.feeling)
    #             self.sons.append(ltm)
    #     self.alpha = 0 # 应该是负数
    #     self.beta = 0
    #     self.gamma = 0
    #     self.delta = 0
    #     return

    def cal_weight(self):
        ans = self.delta
        ans += self.alpha * (self.satisfaction)
        for ltm in self.lowlevel_ltms:
            ans += self.beta * sum([tmp.satisfaction for tmp in self.sons])
        for ltm in self.sons:
            ans += self.gamma * sum([tmp.satisfaction for tmp in self.sons])
        return ans
class LOVE(LTM):
    def __init__(self,lowlevelltms):
        LTM.__init__(self)
        self.feeling = 'love'
        self.lowlevel_ltms = lowlevelltms
        self.sons = ['personal safety','sexy']
        for ltm in self.lowlevel_ltms:
            if self.sons.__contains__(ltm.feeling):
                self.sons.remove(ltm.feeling)
                self.sons.append(ltm)
        self.alpha = 0 # 应该是负数
        self.beta = 0
        self.gamma = 0
        self.delta = 0
        return

    def cal_weight(self):
        ans = self.delta
        ans += self.alpha * (self.satisfaction)
        for ltm in self.lowlevel_ltms:
            ans += self.beta * sum([tmp.satisfaction for tmp in self.sons])
        for ltm in self.sons:
            ans += self.gamma * sum([tmp.satisfaction for tmp in self.sons])
        return ans

# 尊重需求
class RESPECT(LTM):
    def __init__(self,lowlevelltms):
        LTM.__init__(self)
        self.feeling = 'respect'
        self.lowlevel_ltms = lowlevelltms
        self.sons = ['family affection','friendship','love']
        for ltm in self.lowlevel_ltms:
            if self.sons.__contains__(ltm.feeling):
                self.sons.remove(ltm.feeling)
                self.sons.append(ltm)
        self.alpha = 0 # 应该是负数
        self.beta = 0
        self.gamma = 0
        self.delta = 0
        return

    def cal_weight(self):
        ans = self.delta
        ans += self.alpha * (self.satisfaction)
        for ltm in self.lowlevel_ltms:
            ans += self.beta * sum([tmp.satisfaction for tmp in self.sons])
        for ltm in self.sons:
            ans += self.gamma * sum([tmp.satisfaction for tmp in self.sons])
        return ans
# 自我实现需求
# unknown