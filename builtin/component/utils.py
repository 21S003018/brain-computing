#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2020/2/19 22:30
@Author  : zsw,cbz
@Site    : https://github.com/1173710224/brain-computing/blob/cbz
@File    : utils.py
@Software: PyCharm
@Descripe: 实现多种skill
"""

import time
import os
import globalvar as gl
import json
import numpy as np
from IO import operate,over


class SKILL():
    def __init__(self,stm):
        self.stm = stm # 只能调用control skill 函数
        return

    def sleep(self,params):
        """
        tired值低于某一阈值的时触发，状态值会有所增加
        :return:None
        """
        def content():
            gl.set_value('signal_sleep',1)
            # 输出开始控制命令
            dic = {}
            dic['operation'] = 'sleep'
            dic = json.dumps(dic)
            file = open(gl.get_value('agentControlPath'), "w")
            file.write(str(dic))
            file.close()
            # 等待agent信号
            rate = 0.5
            while(gl.get_value('signal_sleep') == 1):
                gl.set_value('tired', gl.get_value('tired') + rate)
                time.sleep(1)
            # 输出结束控制命令
            dic = {}
            dic['command'] = 'sleep over'
            file = open(gl.get_value('agentControlPath'), "w")
            file.write(str(json.dumps(dic)))
            file.close()
            return
        from threading import Thread
        problem_detect_thread = Thread(target=content)
        problem_detect_thread.setDaemon(True)
        problem_detect_thread.start()
        return


    def move(self,params):
        # 设置参数
        theta = params['theta']
        phi = params['phi']
        speed = None
        print("moving!")
        try:
            speed = params['speed']
        except:
            speed = 1
        """
        移动
        :param theta: 球坐标-[0,2pi]
        :param phi: 球坐标[0,pi]
        :param speed: number
        :return:
        """
        def content():
            gl.set_value('signal_move',1)
            """
            向环境传递移动信息
            """
            dic = {"operation": "move", "param1": theta, "param2": phi,"param3": speed}
            dic = json.dumps(dic)
            file = open(gl.get_value('agentControlPath'), "w")
            file.write(str(dic))
            file.close()
            while gl.get_value('signal_move') == 1:
                time.sleep(1)
            dic = {}
            dic['command'] = 'move over'
            file = open(gl.get_value('agentControlPath'), "w")
            file.write(str(json.dumps(dic)))
            file.close()
            return
        from threading import Thread
        problem_detect_thread = Thread(target=content)
        problem_detect_thread.setDaemon(True)
        problem_detect_thread.start()
        return


    def observe(self,params):
        """
        传递观察命令
        正常情况下agent一直在进行视觉的信息提取
        但是在执行观察命令之后agent会获得更多的视觉信息
        """
        angle = params['angle']
        def content():
            gl.set_value('signal_observe', 1)
            dic = {"operation": "observe", "param1": angle}
            dic = json.dumps(dic)
            file = open(gl.get_value('agentControlPath'), "w")
            file.write(str(dic))
            file.close()

            '''检索视觉信息,发现target'''
            while gl.get_value('signal_move') == 1:
                print("observing!")
                time.sleep(1)
            file = open(gl.get_value('agentControlPath'), "w")
            dic = {}
            dic['command'] = 'observe over'
            file.write(str(json.dumps(dic)))
            file.close()
            return
        from threading import Thread
        problem_detect_thread = Thread(target=content)
        problem_detect_thread.setDaemon(True)
        problem_detect_thread.start()
        return

    def go(self,params):
        # 设置参数
        x = params['x']
        y = params['y']
        def content():
            # gl.set_value('signal_move', 1)
            """
            向环境传递移动信息
            """
            operate('go',[x,y])
            # while gl.get_value('signal_move') == 1:
            time.sleep(1)
            over('go')
            return
        content()
        # from threading import Thread
        # problem_detect_thread = Thread(target=content)
        # problem_detect_thread.setDaemon(True)
        # problem_detect_thread.start()
        return
    def call(self,message):
        def content():
            # gl.set_value('signal_move', 1)
            """
            向环境传递移动信息
            """
            operate('call',[message])
            # while gl.get_value('signal_move') == 1:
            time.sleep(1)
            over('call')
            return
        content()
        # from threading import Thread
        # problem_detect_thread = Thread(target=content)
        # problem_detect_thread.setDaemon(True)
        # problem_detect_thread.start()
        return

    def note(self):
        def content():
            # gl.set_value('signal_move', 1)
            """
            向环境传递移动信息
            """
            operate('note',[])
            # while gl.get_value('signal_move') == 1:
            time.sleep(1)
            over('note')
            return
        content()
        # from threading import Thread
        # problem_detect_thread = Thread(target=content)
        # problem_detect_thread.setDaemon(True)
        # problem_detect_thread.start()
        return


    def eat(self,params):
        food_type = params['food_type']
        def content():
            gl.set_value('signal_eat',1)
            """
            向环境传递睡觉信息
            """
            dic = {"operation": "eat","param1": food_type}
            dic = json.dumps(dic)
            file = open(gl.get_value('agentControlPath'), "w")
            file.write(str(dic))
            file.close()
            rate = 0.1
            while(gl.get_value('signal_eat') == 1):
                gl.set_value('hungry', gl.get_value('hungry') + rate)
                time.sleep(1)
            file = open(gl.get_value('agentControlPath'), "w")
            dic = {}
            dic['command'] = 'eat over'
            file.write(str(json.dumps(dic)))
            file.close()
            return

        from threading import Thread
        problem_detect_thread = Thread(target=content)
        problem_detect_thread.setDaemon(True)
        problem_detect_thread.start()
        return



    def drink(self,params):
        drink_type = params['drink_type']
        def content():
            gl.set_value('signal_drink',1)
            """
            向环境传递睡觉信息
            """
            dic = {"operation": "drink","param1": drink_type}
            dic = json.dumps(dic)
            file = open(gl.get_value('agentControlPath'), "w")
            file.write(str(dic))
            file.close()
            rate = 0.5
            while(gl.get_value('signal_drink') == 1):
                gl.set_value('thirsty', gl.get_value('thirsty') + rate)
                time.sleep(1)
            file = open(gl.get_value('agentControlPath'), "w")
            dic = {}
            dic['command'] = 'drink over'
            file.write(str(json.dumps(dic)))
            file.close()
            return

        from threading import Thread
        problem_detect_thread = Thread(target=content)
        problem_detect_thread.setDaemon(True)
        problem_detect_thread.start()
        return


    def sex(self,params):
        sex_target = params['sex_target']
        def content():
            gl.set_value('signal_sex',1)
            """
            向环境传递睡觉信息
            """
            dic = {"operation": "sex","param1": sex_target}
            dic = json.dumps(dic)
            file = open(gl.get_value('agentControlPath'), "w")
            file.write(str(dic))
            file.close()
            rate = 0.5
            while(gl.get_value('signal_sex') == 1):
                gl.set_value('sexy', gl.get_value('sexy') + rate)
                time.sleep(1)
            file = open(gl.get_value('agentControlPath'), "w")
            dic = {}
            dic['command'] = 'sex over'
            file.write(str(json.dumps(dic)))
            file.close()
            return

        from threading import Thread
        problem_detect_thread = Thread(target=content)
        problem_detect_thread.start()
        return


    def search(self,params):
        """
        边move边observe
        """
        params['angle'] = 120
        def content():
            gl.set_value('signal_search', 1)
            '''搜索target'''
            self.observe(params)
            self.stm.think_control_skill('observe')
            while gl.get_value('signal_search') == 1:
                if gl.get_value('find') == 1:
                    params['theta'] = 0
                    params['phi'] = 0
                else:
                    params['theta'] = 0.
                    params['phi'] = float(np.random.randint(0, 360, 1)[0])
                self.move(params)
                self.stm.think_control_skill('move')
                time.sleep(1)
                gl.set_value('signal_move',0)
            file = open(gl.get_value('agentControlPath'), "w")
            dic = {}
            dic['command'] = 'search over'
            file.write(str(json.dumps(dic)))
            file.close()
            return
        from threading import Thread
        problem_detect_thread = Thread(target=content)
        problem_detect_thread.start()
        return



    '''
    收集物体进背包
    '''
    def collect(self, params):
        knapsack = params['knapsack']
        def content():
            """
            向环境传递移动信息
            """
            print(gl.get_value('name') + " is going to collect ")
            file = open(gl.get_value('agentControlPath'), "w")
            dic = {"operation": "collect","param1": knapsack}
            dic = json.dumps(dic)
            file.write(str(dic))
            file.close()

            while gl.get_value('signal_collect') == 1:
                print("try to collect")
                time.sleep(1)
            dic = {}
            dic['command'] = 'collect over'
            dic['knapsack'] = gl.get_value(gl.get_value('name')+'_knapsack')
            file.write(str(json.dumps(dic)))
            file.close()
            return

        from threading import Thread
        problem_detect_thread = Thread(target=content)
        problem_detect_thread.setDaemon(True)
        problem_detect_thread.start()
        return

    #从环境中拿东西到身体包
    def getFromEnv(self, params):
        bodybag = params['bodybag']
        def content():
            """
            向环境传递移动信息
            """
            print(gl.get_value('name') + " is going to getFromEnv ")
            file = open(gl.get_value('agentControlPath'), "w")
            dic = {"operation": "getFromEnv","param1": bodybag}
            dic = json.dumps(dic)
            file.write(str(dic))
            file.close()

            while gl.get_value('signal_getFromEnv') == 1:
                print("try to getFromEnv")
                time.sleep(1)
            dic = {}
            dic['command'] = 'getFromEnv over'
            dic['bodybag'] = gl.get_value(gl.get_value('name')+'_bodybag')
            file.write(str(json.dumps(dic)))
            file.close()
            return

        from threading import Thread
        problem_detect_thread = Thread(target=content)
        problem_detect_thread.setDaemon(True)
        problem_detect_thread.start()
        return

    #从背包中拿出东西到身体包
    def getFromBag(self, params):
        knapsack = params['knapsack']
        bodybag = params['bodybag']
        def content():
            """
            向环境传递移动信息
            """
            print(gl.get_value('name') + " is going to getFromBag ")
            file = open(gl.get_value('agentControlPath'), "w")
            dic = {"operation": "getFromBag","param1": knapsack, "param2": bodybag}
            dic = json.dumps(dic)
            file.write(str(dic))
            file.close()

            while gl.get_value('signal_getFromBag') == 1:
                print("try to getFromBag")
                time.sleep(1)
            dic = {}
            dic['command'] = 'getFromBag over'
            dic['knapsack'] = gl.get_value(gl.get_value('name')+'_knapsack')
            dic['bodybag'] = gl.get_value(gl.get_value('name')+'_bodybag')
            file.write(str(json.dumps(dic)))
            file.close()
            return

        from threading import Thread
        problem_detect_thread = Thread(target=content)
        problem_detect_thread.setDaemon(True)
        problem_detect_thread.start()
        return


#
# def defense(tool, target_x, target_y, target_z):
#     def content():
#         """
#         防御
#         """
#         print(gl.get_value('name') + "is going to defense!")
#         file = open(gl.get_value('agentControlPath'), "w")
#         dic = {}
#         dic[1] = {"operation": "defense", "param1": target_x, "param2": target_y, "param3": target_z}
#         import json
#         dic = json.dumps(dic)
#         file.write(str(dic))
#         file.close()
#         timeStamp = os.stat(gl.get_value('agentControlPath')).st_mtime
#         while timeStamp == os.stat(gl.get_value('agentControlPath')).st_mtime:
#             import time
#             time.sleep(1)
#         return
#
#     from threading import Thread
#     problem_detect_thread = Thread(target=content)
#     problem_detect_thread.setDaemon(True)
#     problem_detect_thread.start()
#     return
#
#
# def attack(tool, target_x, target_y, target_z):
#     def content():
#         """
#         函数开始提示信息
#         """
#         print(gl.get_value('name') + " take attacking!")
#         """
#         向环境传递控制信息
#         """
#         dic = {}
#         dic[1] = {"operation": "attack", "param1": tool, "param2": target_x, "param3": target_y, "param4": target_z}
#         import json
#         dic = json.dumps(dic)
#         file = open(gl.get_value('agentControlPath'), "w")
#         file.write(str(dic))
#         file.close()
#         timeStamp = os.stat(gl.get_value('agentControlPath')).st_mtime
#         """
#         等待环境执行结束
#         """
#         while timeStamp == os.stat(gl.get_value('agentControlPath')).st_mtime:
#             print('st_mtime')
#             print(os.stat(gl.get_value('agentControlPath')).st_mtime)
#             import time
#             time.sleep(1)
#         """
#         TODO
#         功能区
#         """
#         print("over!")
#         return
#
#     from threading import Thread
#     problem_detect_thread = Thread(target=content)
#     problem_detect_thread.setDaemon(True)
#     problem_detect_thread.start()
#     return
#
#
# def give_up(target_x, target_y, target_z):
#     def content():
#         """
#         函数开始提示信息
#         """
#         print(gl.get_value('name') + " give up!")
#         """
#         向环境传递控制信息
#         """
#         dic = {}
#         dic[1] = {"operation": "give_up", "param1": target_x, "param2": target_y, "param3": target_z}
#         import json
#         dic = json.dumps(dic)
#         file = open(gl.get_value('agentControlPath'), "w")
#         file.write(str(dic))
#         file.close()
#         timeStamp = os.stat(gl.get_value('agentControlPath')).st_mtime
#         """
#         等待环境执行结束
#         """
#         while timeStamp == os.stat(gl.get_value('agentControlPath')).st_mtime:
#             print('st_mtime')
#             print(os.stat(gl.get_value('agentControlPath')).st_mtime)
#             import time
#             time.sleep(1)
#         """
#         TODO
#         功能区
#         """
#         print("over!")
#         return
#
#     from threading import Thread
#     problem_detect_thread = Thread(target=content)
#     problem_detect_thread.setDaemon(True)
#     problem_detect_thread.start()
#     return
#
#
# def chat(target):
#     def content():
#         """
#         函数开始提示信息
#         """
#         print(gl.get_value('name') + " is trying to chat " + str(target))
#         """
#         向环境传递控制信息
#         """
#         dic = {}
#         dic[1] = {"operation": "chat", "param1": target}
#         import json
#         dic = json.dumps(dic)
#         file = open(gl.get_value('agentControlPath'), "w")
#         file.write(str(dic))
#         file.close()
#         timeStamp = os.stat(gl.get_value('agentControlPath')).st_mtime
#         """
#         等待环境执行结束
#         """
#         while timeStamp == os.stat(gl.get_value('agentControlPath')).st_mtime:
#             print('st_mtime')
#             print(os.stat(gl.get_value('agentControlPath')).st_mtime)
#             import time
#             time.sleep(1)
#         """
#         TODO
#         功能区
#         """
#         print("Good bye!")
#         return
#
#     from threading import Thread
#     problem_detect_thread = Thread(target=content)
#     problem_detect_thread.setDaemon(True)
#     problem_detect_thread.start()
#     return
#
#
# def care(target):
#     def content():
#         """
#         函数开始提示信息
#         """
#         print(gl.get_value('name') + " is trying to care " + str(target))
#         """
#         向环境传递控制信息
#         """
#         dic = {}
#         dic[1] = {"operation": "care", "param1": target}
#         import json
#         dic = json.dumps(dic)
#         file = open(gl.get_value('agentControlPath'), "w")
#         file.write(str(dic))
#         file.close()
#         timeStamp = os.stat(gl.get_value('agentControlPath')).st_mtime
#         """
#         等待环境执行结束
#         """
#         while timeStamp == os.stat(gl.get_value('agentControlPath')).st_mtime:
#             print('st_mtime')
#             print(os.stat(gl.get_value('agentControlPath')).st_mtime)
#             import time
#             time.sleep(1)
#         """
#         TODO
#         功能区
#         """
#         print("Yeap!")
#         return
#
#     from threading import Thread
#     problem_detect_thread = Thread(target=content)
#     problem_detect_thread.setDaemon(True)
#     problem_detect_thread.start()
#     return
#
#
# def make_new_friends(target):
#     def content():
#         """
#         函数开始提示信息
#         """
#         print(gl.get_value('name') + " is trying to make friends with " + str(target))
#         """
#         向环境传递控制信息
#         """
#         dic = {}
#         dic[1] = {"operation": "mnf", "param1": target}
#         import json
#         dic = json.dumps(dic)
#         file = open(gl.get_value('agentControlPath'), "w")
#         file.write(str(dic))
#         file.close()
#         timeStamp = os.stat(gl.get_value('agentControlPath')).st_mtime
#         """
#         等待环境执行结束
#         """
#         while timeStamp == os.stat(gl.get_value('agentControlPath')).st_mtime:
#             print('st_mtime')
#             print(os.stat(gl.get_value('agentControlPath')).st_mtime)
#             import time
#             time.sleep(1)
#         """
#         TODO
#         功能区
#         """
#         print("Yeap!")
#         return
#
#     from threading import Thread
#     problem_detect_thread = Thread(target=content)
#     problem_detect_thread.setDaemon(True)
#     problem_detect_thread.start()
#     return
#
#
# """
# TODO
# 需要调用语言处理机制
# 发送控制命令，向某人发送请求，请求某物
# 详细解释请见协议
# """
#
#
# def func1(target, agent):
#     def content():
#         """
#         函数开始提示信息
#         """
#         print(gl.get_value('name') + " is trying to get something from " + str(agent))
#         """
#         向环境传递控制信息
#         """
#         dic = {}
#         dic[1] = {"operation": "func1", "param1": target, "param2": agent}
#         import json
#         dic = json.dumps(dic)
#         file = open(gl.get_value('agentControlPath'), "w")
#         file.write(str(dic))
#         file.close()
#         timeStamp = os.stat(gl.get_value('agentControlPath')).st_mtime
#         """
#         等待环境执行结束
#         """
#         while timeStamp == os.stat(gl.get_value('agentControlPath')).st_mtime:
#             print('st_mtime')
#             print(os.stat(gl.get_value('agentControlPath')).st_mtime)
#             import time
#             time.sleep(1)
#         """
#         TODO
#         功能区
#         """
#         print("Thank you!")
#         return
#
#     from threading import Thread
#     problem_detect_thread = Thread(target=content)
#     problem_detect_thread.setDaemon(True)
#     problem_detect_thread.start()
#     return
#
#
# '''
# TODO
# 具体思考并进行讨论实现
# 需要传递哪些控制命令
# 需要对自己的状态进行哪些更改
# 与别人合作某件事情
# '''
#
#
# def func2(target, agent):
#     def content():
#         """
#         函数开始提示信息
#         """
#         print(gl.get_value('name') + " is trying to cooperate with " + str(agent))
#         """
#         向环境传递控制信息
#         """
#         dic = {}
#         dic[1] = {"operation": "func2", "param1": target, "param2": agent}
#         import json
#         dic = json.dumps(dic)
#         file = open(gl.get_value('agentControlPath'), "w")
#         file.write(str(dic))
#         file.close()
#         timeStamp = os.stat(gl.get_value('agentControlPath')).st_mtime
#         """
#         等待环境执行结束
#         """
#         while timeStamp == os.stat(gl.get_value('agentControlPath')).st_mtime:
#             print('st_mtime')
#             print(os.stat(gl.get_value('agentControlPath')).st_mtime)
#             import time
#             time.sleep(1)
#         """
#         功能区
#         """
#         print("happy to cooperate!")
#         return
#
#     from threading import Thread
#     problem_detect_thread = Thread(target=content)
#     problem_detect_thread.setDaemon(True)
#     problem_detect_thread.start()
#     return
