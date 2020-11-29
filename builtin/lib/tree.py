#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2020/2/19 22:30
@Author  : zsw
@Site    : https://github.com/1173710224/brain-computing/blob/cbz
@File    : tree.py
@Software: PyCharm
@Descripe: 实现uptree和downtree
"""
import globalvar as gl
from queue import Queue
from threading import Thread
import time
SLEEPTIME = 1


class Trunk():
    def __init__(self,address,gist,weight,intensity,mood):
        self.address = address
        self.gist = gist
        self.weight = weight
        self.intensity = intensity
        self.mood = mood
        self.LeftChild = None
        self.RightChild = None
    def set(self,address,gist,weight,intensity,mood):
        self.address = address
        self.gist = gist
        self.weight = weight
        self.intensity = intensity
        self.mood = mood


class UpDownTree():
    def __init__(self,stm,ltms):
        self.root = None
        self.stm = stm # 保存stm的地址
        self.ltms = {} # 保存从address到ltm的映射
        self.inhibition = 0 # 抑制程度
        # 建树
        seq = 0
        num = 2 * len(ltms) - 1
        for seq in range(1,num + 1):
            if seq == 2:
                self.add(seq,None,0,0,0)
            else:
                self.add(seq, None, 0, 0, 0)
        # 给ltm绑定address
        for i in range(len(ltms),2 * len(ltms)):
            ltms[i - len(ltms)].address = i
            self.ltms[i] = ltms[i - len(ltms)]
        # 检测树的结构
        self.travel()
        # 启动
        Thread(target=self.start).start()
        return

    def start(self):
        while True:
            time.sleep(1)
            self.update()
            # print('root',self.root.weight,self.root.gist)
            if self.root == None: # 如果根包含空trunk，跳过
                continue
            if self.root.weight < 5 or gl.get_value(self.root.gist) > 10: # 如果权值小于5，跳过
                continue
            self.stm.tree_add(self.root.gist,'need')

    def add(self,address,gist,weight,intensity,mood):
        if self.root is None:
            self.root = Trunk(address,gist,weight,intensity,mood)
        else:
            queue = []
            queue.append(self.root)
            while len(queue) > 0:
                node = queue.pop(0)
                if not node.LeftChild:
                    node.LeftChild = Trunk(address,gist,weight,intensity,mood)
                    return
                else:
                    queue.append(node.LeftChild)
                if not node.RightChild:
                    node.RightChild = Trunk(address,gist,weight,intensity,mood)
                    return
                else:
                    queue.append(node.RightChild)

    def uptree(self,tmp):
        if tmp.LeftChild and tmp.RightChild:
            self.up(tmp, tmp.LeftChild, tmp.RightChild)
            self.uptree(tmp.LeftChild)
            self.uptree(tmp.RightChild)
        else:
            tmp.address = self.ltms[tmp.address].address
            tmp.gist = self.ltms[tmp.address].feeling
            tmp.intensity = gl.get_value(self.ltms[tmp.address].feeling) - self.inhibition
            tmp.weight = 10 - tmp.intensity
            tmp.mood = tmp.intensity
        return
    '''
    l,r是o的两个子节点，请根据l,r更新o中的chunk,假设l,r刚刚更新完毕
    '''
    def up(self,o,l,r):
        # print('l',l.weight,l.gist)
        # print('r',r.weight,r.gist)
        if l.weight >= r.weight:
            o.address, o.gist, o.weight, o.intensity, o.mood = l.address, l.gist, l.weight,\
                                                     l.intensity + r.intensity, \
                                                     l.mood + r.mood
        else:
            o.address, o.gist, o.weight, o.intensity, o.mood = r.address, r.gist, r.weight,\
                                                     l.intensity + r.intensity, \
                                                     l.mood + r.mood
        return

    def downtree(self):
        def content():
            self.inhibition = 1
            time.sleep(5)
            self.inhibition = 0
            return
        from threading import Thread
        problem_detect_thread = Thread(target=content)
        problem_detect_thread.setDaemon(True)
        problem_detect_thread.start()
        return

    def travel(self):
        if self.root is None:
            return
        queue = Queue()
        queue.put(self.root)
        while queue.qsize() > 0:
            node = queue.get()
            # print(str(node.address))
            if node.LeftChild:
                queue.put(node.LeftChild)
                # print(str(node.LeftChild.address))
            if node.RightChild:
                queue.put(node.RightChild)
                # print(str(node.RightChild.address))
            # print()

    def getLeaves(self):
        list = []
        if self.root is None:
            return list
        queue = []
        queue.append(self.root)
        while len(queue) > 0:
            node = queue.pop(0)
            if node.LeftChild:
                queue.append(node.LeftChild)
            if node.RightChild:
                queue.append(node.RightChild)
            if not node.LeftChild:
                list.append(node.address)
        return list

    def update(self):
        '''
        返回更新之后root中的gist
        :return:
        '''
        self.uptree(self.root)
        return self.root

    def setLeaf(self,address,gist,weight,intensity,mood):
        if self.root is None:
            return list
        queue = []
        queue.append(self.root)
        while len(queue) > 0:
            node = queue.pop(0)
            if node.address == address:
                node.set(address,gist,weight,intensity,mood)
            if node.LeftChild:
                queue.append(node.LeftChild)
            if node.RightChild:
                queue.append(node.RightChild)

    def getintensity(self,feeling):
        for tmp in self.ltms:
            if self.ltms[tmp].feeling == feeling:
                return
        return None