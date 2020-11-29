#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2020/2/21 22:58
@Author  : cbz
@Site    : https://github.com/1173710224/brain-computing/blob/cbz
@File    : stmcache.py
@Software: PyCharm
@Descripe: slots实现
"""
import globalvar as gl
import time
# 定义规则以及常量
inf = 1000000000
# slot 有四种类型：method,need,object,ontology
# relation 有五种类型：feel,solvedby,rely + own,note
# 一条用于测试的逻辑序列
testsequence = "apple,search,eat,hungry"


class SLOT():
    def __init__(self,label,type,intensity = 0,father = None):
        self.intensity = intensity
        self.label = label
        self.type = type
        self.father = father
        self.son = None
        return

    def __eq__(self, other):
        return other.label == self.label and self.type == other.type

    def __hash__(self):
            return hash(self.label) * 10 + hash(self.type)


class ONTOLOGY(SLOT):
    def __init__(self,label,type):
        SLOT.__init__(self,label,type)
        self.son = set()
        return


class SLOTS():
    def __init__(self,kg):
        self.core = set() # 集合中只维护所有的非父亲结点
        self.kg = kg # 知识库接口
        self.threshold = 7 # 短时记忆存储容量的上限
        self.core.add(ONTOLOGY('self','ontology')) # 将self添加进slots
        return

    # TODO:这里从source出发判断一个slot可能有点问题
    def add(self,label,type,source = None,relation=None):
        """
        向stm中添加一个slot
        :param label: slot的label
        :param type: slot的type
        :param source: 父亲slot的label
        :return: True if add successfully, esle False
        """
        father = self.get_slot(source)
        tmp = SLOT(label,type,father)
        # 判断是否已经存在与slots中
        if self.is_exists(tmp):
            return False
        # 计算强度
        if not father:
            intensity = self.calintensity(tmp)
            tmp.intensity = intensity
        else:
            tmp.intensity = father.intensity
        # 判断是否可加入
        tmpminslot = self.minintensity()
        if self.fullload() and tmp.intensity <= tmpminslot.intensity:
            return False
        if self.fullload():
            self.core.remove(tmpminslot)
        # 添加操作
        if not father:
            self.core.add(tmp)
        else:
            if source == 'self':
                father.son.add((relation,tmp))
                tmp.father = father
                self.core.add(tmp)
            else:
                father.son = tmp
                tmp.father = father
                self.core.remove(father)
                self.core.add(tmp)
        return True

    # TODO：需要重写
    def addslot(self,slot):
        """
        将slot加入slots
        :param slot:
        :return:
        """
        while slot.father:
            self.add(slot.label,slot.type,slot.father.label)
            slot = slot.father
        self.add(slot.label,slot.type)
        return

    def remove(self,label,type):
        """
        按照label将slot进行移除
        :param label:
        :return: True if remove successfully
        """
        print('run remove method',label,type)
        path = [] # 测试用
        for slot in self.core:
            head = slot
            path.append(slot.label)
            while slot.label != 'self':
                if slot.label == label and slot.type == type:
                    self.core.remove(head)
                    self.core.add(slot.father)
                    print('logic sequence removed path :',path)
                    return True
                slot = slot.father
                print(slot)
                path.append(slot.label)
        return False

    # TODO：将计算强度的函数补充完整，目前返回一个固定值
    def calintensity(self,slot):
        """
        计算当前slot对agent的刺激程度，使用强度进行表示
        :param slot: 计算对象
        :return: number
        """
        return 1

    def minintensity(self):
        """
        计算所有slot强度的最小的slot
        :return: slot type
        """
        ret = inf
        ans = None
        for slot in self.core:
            if slot.intensity < ret:
                ret = slot.intensity
                ans = slot
        return ans

    # TODO：对slots进行降维处理，理论结果，目前只针对特殊逻辑序列进行简单检测
    # TODO:在当前的测验中，假设search之后已经get到需要吃的东西了
    def reduction(self,slot):
        """
        slots降维处理
        :return: None
        """
        temp = None
        for tmp in self.core:
            if tmp == slot:
                continue
            if tmp.label == slot.label:
                temp = tmp
        while gl.get_value('signal_search') == 1:
            time.sleep(1)
        self.remove(temp.label,temp.type)
        temp = temp.father
        temp = temp.father
        self.addslot(temp)
        self.remove(slot.label,slot.type)
        self.add(slot.label,slot.type,temp.label)
        return

    def calnum(self):
        """
        计算当前slots中总个数
        :return: number
        """
        num = 0
        for slot in self.core:
            num += len(self.traverse(slot))
        return num

    def fullload(self):
        """
        判断slots是不是已经满了
        :return:
        """
        if self.calnum() == self.threshold:
            return True
        return False

    def get_slot(self,label):
        """
        计算label对应的slot
        :param label: 某个slot的label
        :return: slot type
        """
        slots = []
        for slot in self.core:
            slots += self.traverse(slot)
        ret = None
        for slot in slots:
            if slot.label == label:
                ret = slot
                break
        return ret

    def traverse(self,slot):
        """
        遍历以slot开始的逻辑序列
        :param slot: 出发几点
        :return: 包含以slot开始的逻辑序列中所有slot的列表
        """
        ret = []
        while slot.father:
            ret.append(slot)
            slot = slot.father
            print('traverse',slot.label)
        ret.append(slot)
        return ret

    def globaltraverse(self):
        """
        全局遍历
        :return: 所有的slot
        """
        ret = []
        for slot in self.core:
            ret += self.traverse(slot)
        return ret

    def get_father(self,obj):
        '''
        返回obj的father的label
        :param obj:
        :return:
        '''
        for slot in self.core:
            if slot.label == obj:
                return slot.father.label
        return None

    def is_exists(self,slot):
        '''
        判断slot是不是存在
        :param slot:
        :return:
        '''
        lis = self.globaltraverse()
        for tmp in lis:
            if tmp == slot:
                return True
        return False