#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2020/2/20 18:03
@Author  : cbz
@Site    : https://github.com/1173710224/brain-computing/blob/cbz
@File    : IO.py
@Software: PyCharm
@Descripe: 
"""
import json
import time
import globalvar as gl


def init():
    """
    初始化文件格式
    :return:
    """
    file = open(gl.get_value('agentControlPath'), 'r')
    try:
        dic = json.load(file)
        lis = dic["operation"]
        for tmp in lis:
            if type(tmp) is not type(''):
                x = 1 / 0
        lis = dic["over"]
        for tmp in lis:
            if type(tmp) is not type(''):
                x = 1 / 0
        if len(dic) > 2:
            x = 1 / 0
        file.close()
    except:
        file.close()
        file = open(gl.get_value('agentControlPath'), 'w')
        dic = {}
        dic['operation'] = []
        dic['over'] = []
        file.write(str(json.dumps(dic)))
        file.close()
        return


def operate(method,params):
    """
    执行操作命令
    :param method: 要执行的skill
    :param params: skill的参数
    :return:None
    """
    # 读取当前命令
    file = open(gl.get_value('agentControlPath'), 'r')
    dic = json.load(file)
    file.close()
    # print('operation',dic)
    flag = False
    for command in dic['operation']:
        # command = ''
        if command.__contains__(method):
            flag = True
    if flag == True:
        return
    # 将method添加到当前命令中
    tmp = method
    for param in params:
        tmp += '\t' + str(param)
    dic['operation'].append(tmp)
    # 将控制命令写回文件
    dic = json.dumps(dic)
    file = open(gl.get_value('agentControlPath'), "w")
    file.write(str(dic))
    file.close()
    print(gl.get_value('name') + ' ' + str(dic))
    # file = open(gl.get_value('agentControlPath'), "r")
    # print('operation',file.readline())
    # file.close()
    return


def over(method):
    """
    结束某skill
    :param method: 将要结束的skill
    :return:None
    """
    # 读取当前的控制命令
    file = open(gl.get_value('agentControlPath'), 'r')
    dic = json.load(file)
    file.close()
    # 将method从控制命令中取消
    # print('over',dic)
    for tmp in dic['operation']:
        if tmp.__contains__(method):
            dic['operation'].remove(tmp)
    # print('over',dic)
    # 为method添加取消控制命令，然后写回文件
    # dic['over'].append(method)
    dic = json.dumps(dic)
    file = open(gl.get_value('agentControlPath'), "w")
    file.write(str(dic))
    file.close()
    # # file = open(gl.get_value('agentControlPath'), "r")
    # # # print('over',file.readline())
    # file.close()
    # 取消命令在文件中保存1s之后去掉
    # time.sleep(1)
    # dic = json.loads(dic)
    # dic['over'].remove(method)
    # dic = json.dumps(dic)
    # file = open(gl.get_value('agentControlPath'), "w")
    # file.write(str(dic))
    # file.close()
    return

# 范式
"""
{"operation":[sequenceA,sequenceA,...,...],"over":[sequenceB,sequenceB,...]}
sequenceA is of string type, and is constructed as: method + "\t" + str(param1) + "\t" + ... + str(paramn)
method is of string type, which represents a skill
parami is the i-th parameter of method
"""
# rules
"""
出现在operation下的是需要执行的
出现在over下的是需要停止的
over命令在控制文件中只出现一秒
"""

# examples
"""
i.e.,{"operation":["sleep","move 40  25  2"],"over":[]}
i.e.,{"operation":["sleep"],"over":["move"]}
"""

# 不会出现的情况
"""
i.e.,{"operation":["sleep"],"over":["sleep"]}
"""