#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2020/2/19 22:30
@Author  : cbz,zsw
@Site    : https://github.com/1173710224/brain-computing/blob/cbz
@File    : stm.py
@Software: PyCharm
@Descripe: 实现stm
"""
from ltm import *
from weightedKG import *
from tree import *
from utils import *
from IO import *
from stmcache import SLOTS,SLOT
from threading import Thread
import time
import json


class STM():
    def __init__(self,name,energy = 5.1):
        self.name = name # 配置姓名
        knapsack = {} # 配置背包
        bodybag = {}
        gl.set_value('name', self.name) # 将名字放在全局变量
        gl.set_value(self.name + '_knapsack', knapsack) # 将背包放在全局变量
        gl.set_value(self.name + '_bodybag', bodybag)  # 将身体包放在全局变量
        gl.configpath(name) # 配置交互文件路径
        self.kg = KnowldgeGraph(name) # 配置知识库
        self.slots = SLOTS(self.kg) # 配置stm缓存，短期记忆
        self.skillLTM = SKILL(self) # 配置skillLTM
        self.sensor = SENSOR(self)
        # OPTICALSENSOR().collectMessage() # 配置sensorLTM
        # SOUNDSENSOR().collectMessage()
        self.feelingLTM = [SLEEP(),ENERGY(energy),WATER(),BREED(),PAIN(),PERSONAL_SAFETY(),FRIENDSHIP()] # 配置feelingLTM
        self.updowntree = UpDownTree(self,self.feelingLTM) # 配置updowntree
        for ltm in self.feelingLTM[:5]: # 开启feelingLTM
            ltm.checkState()
        self.__detect_life() # 开始检测生命结束
        return

    def __process_need(self,need):
        '''
        对需求进行处理
        :param need:
        :return:
        '''
        method = self.__think_find_method(need)
        self.slots.add(method,'method',need) # 添加slot
        feasibility = self.__think_canexe(method)
        print(self.name, method,feasibility)
        if feasibility == True:
            params = self.__think_cal_params(method)
            eval('self.skillLTM.' + method)(params)
            self.think_control_skill(method)
            while gl.get_value('signal_' + method) == 1:
                time.sleep(1)
        else:
            self.slots.add(feasibility,'need',method) # 添加slot
            self.__process_need(feasibility)
            params = self.__think_cal_params(method)
            eval('self.skillLTM.' + method)(params)
            self.think_control_skill(method)
            while gl.get_value('signal_' + method) == 1:
                time.sleep(1)
        return

    def process_message(self,message):
        # message = {}
        # print('processmessage')
        message_h = message['hearing']
        if message_h == 'danger':
            eval('self.skillLTM.note')()

        message = message['vision']
        if message.__contains__('predator') and message.__contains__('agent'):
            gl.set_value('friendship', np.sqrt((message['predator']['x'] - message['agent']['x']) ** 2 + (
                        message['predator']['y'] - message['agent']['y']) ** 2) * 0.2)
        if message.__contains__('predator'):
            gl.set_value('personal safety',np.sqrt(message['predator']['x']**2 + message['predator']['y']**2) * 0.3)

        if self.slots.is_exists(SLOT(label='hungry', type='need')):
            if message.__contains__('prey'):
                # Thread(target=self.__process_hungry, args=(message['prey']['x'], message['prey']['y'],)).start()  # 对需求进行处理
                self.__process_hungry(message['prey']['x'], message['prey']['y'])  # 对需求进行处理
        elif self.slots.is_exists(SLOT(label='personal safety', type='need')):
            if not message.__contains__('predator'):
                self.slots.core.remove(SLOT(label='personal safety', type='need'))
                if gl.get_value('personal safety') < 5:
                    gl.set_value('personal safety',10)
            else:
                # Thread(target=self.__process_safety, args=(message['predator']['x'], message['predator']['y'],)).start()  # 对需求进行处理
                self.__process_safety(message['predator']['x'], message['predator']['y'])  # 对需求进行处理
        elif self.slots.is_exists(SLOT(label='friendship', type='need')):
            if not (message.__contains__('predator') or message.__contains__('agent')):
                self.slots.core.remove(SLOT(label='friendship', type='need'))
                if gl.get_value('friendship') < 5:
                    gl.set_value('friendship',10)
            else:
               self.__process_ship()
        return

    def __process_hungry(self,x,y):
        if abs(x) + abs(y) < 0.1:
            gl.set_value('hungry', gl.get_value('hungry') + 10)
            self.slots.core.remove(SLOT(label='hungry',type='need'))
            return
        dis = np.sqrt(x**2 + y**2)
        v = 1
        if v > dis:
            eval('self.skillLTM.go')({'x': x, 'y': y})
            return
        eval('self.skillLTM.go')({'x':v / dis * x,'y':v / dis * y})
        return

    def __process_safety(self,x,y):
        if abs(x) + abs(y) < 0.1:
            gl.set_value('pain', -1)
            return
        dis = np.sqrt(x**2 + y**2)
        alpha = 0.1
        beta = 0.1
        intensity = 10 - gl.get_value('personal safety')
        v = alpha * gl.get_value('hungry') + beta * intensity
        print(dis,x,y)
        if v > dis:
            eval('self.skillLTM.go')({'x': x, 'y': y})
            return
        eval('self.skillLTM.go')({'x':-v / dis * x,'y':-v / dis * y})
        return

    def __process_ship(self):
        eval('self.skillLTM.call')('danger')
        return

    def sensor_add(self,label):
        '''
        感知器向slots中添加一个slot
        :return:
        '''
        if self.slots.add(label,type='object',relation='note'): # 在slots中添加slot
            print(self.name,'notes ' + label + ' in the environment!')
        return

    def tree_add(self,label,type):
        '''
        updowntree向slots中添加一个slot,tree添加的应该都是need类型的
        :return:
        '''
        if self.slots.add(label,type,relation='feel'): # 在slots中添加slot
            # print(self.name,'start processing need!')
            print(self.name,label)
            # Thread(target=self.__process_need,args=(label,)).start() # 对需求进行处理
        return

    def __detect_life(self):
        """
        判断生命是否结束，如果结束直接切进程
        :return:None
        """
        def content():
            while True:
                die = False
                ans = {}
                ans['tired'] = gl.get_value('tired')
                ans['hungry'] = gl.get_value('hungry')
                ans['thirsty'] = gl.get_value('thirsty')
                ans['pain'] = gl.get_value('pain')
                ans['sexy'] = gl.get_value('sexy')
                ans['personal safety'] = gl.get_value('personal safety')
                ans['friendship'] = gl.get_value('friendship')
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
                    cmd = "taskkill /F /PID " + str(os.getpid())
                    os.system(cmd)
                time.sleep(1)
                print(self.name + ' ' + str(ans))

        from threading import Thread
        state_update_thread = Thread(target=content)
        state_update_thread.setDaemon(True)
        state_update_thread.start()

    def __think_find_method(self,need):
        '''
        针对当前需求返回一个解决办法
        :param need: 待解决的需求
        :return:
        '''
        # # 搜索能解决当前问题的方法--
        # methods = self.kg.querymethod(need)
        # print('methods', methods)
        # # 通过模拟计算出当前状态下最好的方法
        # bestMethod = None
        # maxReward = 0
        # for x in methods:
        #     self.kg.setFactor1(x, 1)
        #     tmpReward = self.kg.calReward('happy')
        #     if maxReward < tmpReward:
        #         bestMethod = x
        #         maxReward = tmpReward
        bestMethod = 'collect'
        return bestMethod

    # change with each method
    def __think_canexe(self,method):
        '''
        判断当前方法是否可行
        :param method:
        :return: (True,None)如果可行，否则(Reason)
        '''
        if method == 'eat':
            ontology = self.slots.get_slot('self')
            for son in ontology.son:
                if son[0] == 'own' and son[1].label == 'apple':
                    return True
        if method == 'search':
            return True
        def think_reason():
            '''
            只有当方法不可行的时候才能调用
            检查不可行的原因
            :return:
            '''
            if method == 'eat':
                return 'apple'
        return think_reason()

    # change with each method
    def __think_cal_params(self,method):
        '''
        计算method执行所需参数
        :param method:方法名
        :return:
        '''
        dic = {}
        if method == 'sleep':
            return dic
        if method == 'move':
            dic['theta'] = 30
            dic['phi'] = 45
            dic['speed'] = 2
            return dic
        if method == 'observe':
            dic['angle'] = 120
            return dic
        if method == 'eat':
            ontology = self.slots.get_slot('self')
            for son in ontology.son:
                if son[0] == 'own':
                    dic['food_type'] = 'apple'
            return dic
        if method == 'drink':
            dic['drink_type'] = 'water'
            return dic
        if method == 'sex':
            dic['sex_target'] = 'Bob'
            return dic
        if method == 'search':
            return dic
        if method == 'collect':
            dic['knapsack'] = gl.get_value(gl.get_value('name')+'_knapsack')
            return dic
        if method == 'getFromEnv':
            dic['bodybag'] = gl.get_value(gl.get_value('name')+'_bodybag')
        if method == 'getFromBag':
            dic['knapsack'] = gl.get_value(gl.get_value('name')+'_knapsack')
            dic['bodybag'] = gl.get_value(gl.get_value('name')+'_bodybag')
        return

    # change with each method
    def think_control_skill(self,method):
        '''
        根据agent自身的状态控制skill执行的结束
        :param method:将要执行的方法名
        :return:
        '''
        def content():
            # 处理sleep函数
            if method == 'sleep':
                while True:
                    file = open(gl.get_value('environmentMessagePath'), 'r')
                    dic = json.load(file)
                    file.close()
                    illuminationMessage = dic['illumination_intensity']
                    decibelMessage = dic['decibel']
                    # print(illuminationMessage,decibelMessage,gl.get_value('tired')) # 函数测试
                    if illuminationMessage > 20 or decibelMessage > 20 or gl.get_value('tired') >= 10:
                        gl.set_value('signal_sleep', 0)
                        break
                    time.sleep(1)
            # 处理eat函数
            if method == 'eat':
                while True:
                    if gl.get_value('hungry') >= 8:
                        self.slots.remove('hungry','need')
                        gl.set_value('signal_eat', 0)
                        break
                    time.sleep(1)
            # 处理drink函数
            if method == 'drink':
                while True:
                    if gl.get_value('thirsty') >= 5:
                        gl.set_value('signal_drink', 0)
                        break
                    time.sleep(1)
            # 处理sex函数
            if method == 'sex':
                while True:
                    if gl.get_value('sexy') >= 5:
                        gl.set_value('signal_sex', 0)
                        break
                    time.sleep(1)
            # 处理move函数
            if method == 'move':
                # 判断终止条件，待更改，目前暂定运行10s
                moveTime = 0
                while True:
                    if moveTime > 10:
                        gl.set_value('signal_move', 0)
                        break
                    time.sleep(1)
                    moveTime += 1
            # 处理observe函数
            if method == 'observe':
                target = 'apple' # 偷个懒，暂做测试用
                num = 0
                while True:
                    num = num + 1
                    file = open(gl.get_value('environmentMessagePath'), 'r')
                    environmentMessage = json.load(file)
                    file.close()
                    if environmentMessage['object_name'] == target:
                        gl.set_value('signal_observe', 0)
                        gl.set_value('find',1)
                        break
                    time.sleep(1)
                    if num > 3 :
                        gl.set_value('signal_observe', 0)
                        gl.set_value('find', 1)
                        break
            #处理search函数
            if method == 'search':
                target = self.slots.get_father(method)
                while True:
                    if gl.get_value('find') == 1:
                        file = open(gl.get_value('environmentMessagePath'), 'r')
                        environmentMessage = json.load(file)
                        file.close()
                        if environmentMessage['distance'] == 0:
                            # 得到苹果并作出相应改变
                            ontology = self.slots.get_slot('self')
                            ontology.son.add(('own',self.slots.get_slot('apple')))
                            # search以及search的target退出slots
                            self.slots.remove(target,'need')
                            gl.set_value('signal_search', 0)
                            break
            if method == 'collect':
                target = 'apple'#测试用
                while True:
                    file = open(gl.get_value('environmentMessagePath'), 'r')
                    environmentMessage = json.load(file)
                    file.close()
                    if environmentMessage['object_name'] == target and environmentMessage['distance'] == 0:
                        dic = gl.get_value(gl.get_value('name')+'_knapsack')
                        if target in dic:
                            dic[target] = dic[target] + 1
                        else:
                            dic[target] = 1
                        gl.set_value(gl.get_value('name')+'_knapsack', dic)
                        gl.set_value('signal_collect', 0)
                        break
                    time.sleep(1)
            if method == 'getFromEnv':
                target = 'apple'#测试用
                while True:
                    file = open(gl.get_value('environmentMessagePath'), 'r')
                    environmentMessage = json.load(file)
                    file.close()
                    if environmentMessage['object_name'] == target and environmentMessage['distance'] == 0:
                        dic = gl.get_value(gl.get_value('name')+'_bodybag')
                        if target in dic:
                            dic[target] = dic[target] + 1
                        else:
                            dic[target] = 1
                        gl.set_value(gl.get_value('name')+'_bodybag', dic)
                        gl.set_value('signal_getFromEnv', 0)
                        break
                    time.sleep(1)
            if method == 'getFromBag':
                target = 'apple'#测试用
                while True:
                    dic1 = gl.get_value(gl.get_value('name')+'_knapsack')
                    dic2 = gl.get_value(gl.get_value('name')+'_bodybag')
                    if target in dic1:
                        if dic1[target] == 1:
                            dic1.pop(target)
                        if dic1[target] > 1:
                            dic1[target] = dic1[target] + 1
                        if target in dic2:
                            dic2[target] = dic2[target] + 1
                        if target not in dic2:
                            dic2[target] = 1
                        gl.set_value(gl.get_value('name')+'_knapsack', dic1)
                        gl.set_value(gl.get_value('name') + '_bodybag', dic2)
                        gl.set_value('signal_getFromBag', 0)
                        break
                    if target not in dic1:
                        print(target + " is not in the knapsack.")
                        gl.set_value('signal_getFromBag', 0)
                    time.sleep(1)
            return

        from threading import Thread
        problem_detect_thread = Thread(target=content)
        problem_detect_thread.setDaemon(True)
        problem_detect_thread.start()
        return

