#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2020/2/19 15:47
@Author  : cbz
@Site    : https://github.com/1173710224/brain-computing/blob/cbz
@File    : test4.py
@Software: PyCharm
@Descripe: 带有权重的知识图谱
"""
from SPARQLWrapper import SPARQLWrapper, JSON
# # 打开fuseki本地服务器
# import os
# os.system("@echo off")
# os.system("java -Xmx1200M -jar fuseki-server.jar")


class vertex(object): # 结点类，对应知识图谱上的实体
    def __init__(self,label,factor1 = 0,factor2 = 0):
        """
        构造函数
        :param label:结点的标签
        :param factor1: 结点的第一个参数
        :param factor2: 结点的第二个参数
        """
        self.__factor1 = factor1
        self.__factor2 = factor2
        self.__label = label
        return

    def __eq__(self,that):
        """
        重写相等函数
        :param that: vertex类型
        :return: True 如果两个vertex实例的label相同，否则返回False
        """
        if self.__label == that.getLabel():
            return True
        return False

    def setFactor1(self,value):
        """
        给factor1赋予一个值
        :param value: factor1的预备值
        :return: None
        """
        self.__factor1 = value
        return

    def setFactor2(self,value):
        self.__factor2 = value
        return

    def getFactor1(self):
        return self.__factor1

    def getFactor2(self):
        return self.__factor2

    def getLabel(self):
        return self.__label


class edge(object): # 有向边类，对应知识图谱中的关系
    def __init__(self,start,target,weight = 0,relation = 'general'):
        """
        构造函数，
        :param start: 边的出发点，类型为vertex
        :param target: 边的终点，类型为vertex
        :param weight: 边的权重
        :param relation: 对应知识图谱中的边所代表的关系
        """
        self.__start = start
        self.__target = target
        self.__weight = weight
        self.__relation = relation
        return

    def __eq__(self,that):
        """
        重写相等函数
        :param that: 另一条边，edge类型
        :return: True 如果出发点、终点、边上的关系都一样，否则返回False
        """
        if self.__start != that.getStart():
            return False
        if self.__target != that.getTarget():
            return False
        if self.__relation != that.getRelation():
            return False
        return True

    def setWeight(self,value):
        self.__weight = value
        return

    def setRelation(self,value):
        self.__relation = value
        return

    def getStart(self):
        return self.__start

    def getTarget(self):
        return self.__target

    def getWeight(self):
        return self.__weight

    def getRelation(self):
        return self.__relation


class KnowldgeGraph(object): # 加权知识图谱的实现
    def __init__(self,name):
        """
        构造函数
        在CCF模型中，每一个agent配置一个加权知识图谱，所以每一个知识图谱都有一个名字
        :param name: agent的名字
        """
        self.name = name
        # 使用入度邻接表和出度邻接表存储图数据
        self.__ingraph = {} # keys包含了所有的target结点
        self.__outgraph = {} # keys包含了所有的start结点
        # fuseki知识图谱增删查改API初始化
        self.__update = SPARQLWrapper("http://localhost:3030/" + self.name + "/update")
        self.__query = SPARQLWrapper("http://localhost:3030/" + self.name + "/query")
        self.__query.setReturnFormat(JSON)
        self.__update.setMethod('POST')
        return

    def addEdge(self,o1,r,o2):
        """
        添加一条边
        :param o1: 出发结点，vertex类型
        :param r: 关系，string类型
        :param o2: 目标结点，vertex类型
        :return: None
        """
        # 更新数据库
        self.__update.setQuery(
        "PREFIX rdf:   <http://www.w3.org/1999/02/22-rdf-syntax-ns#>"
        +"PREFIX ex:   <http://example.org/>"
        +"INSERT DATA {"
        +"ex:" + o1 + "        rdf:" + r + "             ex:" + o2 + "     ."
        +"}")
        self.__update.query()
        # 修改内存中的图
        vertex1 = vertex(label = o1)
        vertex2 = vertex(label = o2)
        _edge = edge(start = vertex1,target = vertex2,relation = r)
        # 修改内存中的图-入度邻接表
        if self.__ingraph.__contains__(vertex2.getLabel()):
            self.__ingraph[vertex2.getLabel()].append(_edge)
        else:
            self.__ingraph[vertex2.getLabel()] = [_edge]
        # 修改内存中的图-出度邻接表
        if self.__outgraph.__contains__(vertex1.getLabel()):
            self.__outgraph[vertex1.getLabel()].append(_edge)
        else:
            self.__outgraph[vertex1.getLabel()] = [_edge]
        return

    def removeEdge(self,o1,r,o2):
        """
        删除一条边
        :param o1: 出发结点，vertex类型
        :param r: 关系，string类型
        :param o2: 目标结点，vertex类型
        :return: None
        """
        # 更新数据库
        self.__update.setQuery(
        "PREFIX rdf:   <http://www.w3.org/1999/02/22-rdf-syntax-ns#>"
        +"PREFIX ex:   <http://example.org/>"
        +"DELETE DATA {"
        +"ex:" + o1 + "        rdf:" + r + "             ex:" + o2 + "     .}")
        self.__update.query()
        # 修改内存中的图
        vertex1 = vertex(label = o1)
        vertex2 = vertex(label = o2)
        # 修改内存中的图-入度邻接表
        if self.__ingraph.__contains__(vertex2.getLabel()) == True:
            for tmp_edge in self.__ingraph[vertex2.getLabel()]:
                if tmp_edge.getStart() == vertex1:
                    self.__ingraph[vertex2.getLabel()].remove(tmp_edge)
                    break
        # 修改内存中的图-出度邻接表
        if self.__outgraph.__contains__(vertex1.getLabel()) == True:
            for tmp_edge in self.__outgraph[vertex1.getLabel()]:
                if tmp_edge.getTarget() == vertex2:
                    self.__outgraph[vertex1.getLabel()].remove(tmp_edge)
                    break
        return

    def queryRelation(self,o1,o2):
        """
        查询两个实体之间的关系
        :param o1: 出发点，string类型
        :param o2: 目标点，string类型
        :return: 包含两个结点之间所有关系的列表
        """
        # 数据库查询
        self.__query.setQuery("PREFIX rdf:   <http://www.w3.org/1999/02/22-rdf-syntax-ns#>"
        +"PREFIX ex:   <http://example.org/>"
        +"SELECT * WHERE {"
        +"ex:" + o1 + "        ?ans             ex:" + o2 + "     ."
        +"}")
        ans = self.__query.query().convert()['results']['bindings']
        # 查询结果处理
        ret = []
        for x in ans:
            ret.append(x['ans']['value'].replace('http://www.w3.org/1999/02/22-rdf-syntax-ns#',''))
        return ret

    def queryO2(self,o1,r):
        """
        根据出发点和关系查询目标点
        :param o1: 出发点，string类型
        :param r: 两个结点之间的关系
        :return: 所有满足条件的结点的label组成的列表
        """
        # 查询数据库
        self.__query.setQuery("PREFIX rdf:   <http://www.w3.org/1999/02/22-rdf-syntax-ns#>"
        +"PREFIX ex:   <http://example.org/>"
        +"SELECT * WHERE {"
        +"ex:" + o1 + "        rdf:" + r + "             ?ans     ."
        +"}")
        tmpans = self.__query.query().convert()['results']['bindings']
        ans = [tmp['ans']['value'].replace('http://example.org/','') for tmp in tmpans]
        # print('ans',ans) # test
        return ans

    def queryO1(self,r,o2):
        self.__query.setQuery("PREFIX rdf:   <http://www.w3.org/1999/02/22-rdf-syntax-ns#>"
        +"PREFIX ex:   <http://example.org/>"
        
        +"SELECT * WHERE {"
        +"?ans        rdf:" + r + "             ex:" + o2 + "     ."
        +"}")
        tmpans = self.__query.query().convert()['results']['bindings']
        ans = [tmp['ans']['value'].replace('http://example.org/','') for tmp in tmpans]
        return ans

    def setFactor1(self,o,x):
        """
        :param o: 要修改的结点，string类型
        :param x: float类型
        :return: None
        """
        for vertex in self.__ingraph:
            if vertex.getLabel() == o:
                vertex.setFactor1(x)
        for vertex in self.__outgraph:
            if vertex.getLabel() == o:
                vertex.setFactor1(x)
        return

    def setFactor2(self,o,x):
        for vertex in self.__ingraph:
            if vertex.getLabel() == o:
                vertex.setFactor2(x)
        for vertex in self.__outgraph:
            if vertex.getLabel() == o:
                vertex.setFactor2(x)
        return

    def setWeight(self,o1,r,o2,x):
        for tmp_edge in self.__ingraph:
            if tmp_edge.getStart().getLabel() == o1:
                tmp_edge.setWeight(x)
                break
        for tmp_edge in self.__outgraph:
            if tmp_edge.getTarget().getLabel() == o2:
                tmp_edge.setWeight(x)
                break
        return

    def querymethod(self,need):
        """
        根据需求查找相应的解决方案
        :param need: 需求名，string类型
        :return: 所有方案构成的列表
        """
        methods = self.queryO2(need,'use')
        return methods

    def queryparams(self,method):
        """
        查询方法的参数
        :param method: skill名字，string类型
        :return: 参数列表
        """
        ans = self.queryO2(method,'parameter')
        return ans

    def calReward(self,method):
        """
        计算method在当前情况下的reward
        :param method: 方法名，string类型
        :return: reward value，float or int type
        """
        # # test
        # if self.__ingraph.__contains__(vertex) == False:
        #     return self.__intensity[vertex]
        # ans = 1
        # for tmp_vertex in self.__ingraph[vertex]:
        #     if self.__factors.__contains__(tmp_vertex) == False:
        #         continue
        #     ans = ans + self.calReward(tmp_vertex) * self.__intensity[tmp_vertex] * self.__factors[tmp_vertex]
        return 1