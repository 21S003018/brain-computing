# -*- coding: utf-8 -*-
"""
Created on Wed Aug 14 20:01:38 2019

@author: cbz
"""

from SPARQLWrapper import SPARQLWrapper, JSON
from stm import STM

'''
head -> vars
results -> bindings -> (type,value)
'''

'''
knowledge是每一个agent默认的初始化知识
'''
knowledge = """
PREFIX rdf:   <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX ex:   <http://example.org/>

INSERT DATA {
ex:stomach        rdf:feeling             ex:hungry     .
ex:brain        rdf:feeling             ex:tired     .
ex:oralCavity        rdf:feeling             ex:thirsty     .
ex:skin        rdf:feeling             ex:pain     .
ex:genitals        rdf:feeling             ex:sexy     .
ex:tired        rdf:use             ex:sleep     .
ex:pick        rdf:parameter1             ex:target     .
ex:hungry        rdf:use             ex:eat     .
ex:apple        rdf:use             ex:search     .
ex:thirsty        rdf:use             ex:collectRainwater     .
ex:collectRainwater        rdf:parameter1             ex:tool     .
ex:collectRainwater        rdf:parameter2             ex:target_x     .
ex:collectRainwater        rdf:parameter3             ex:target_y     .
ex:collectRainwater        rdf:parameter4             ex:target_z     .
ex:thirsty        rdf:use             ex:fetchWater     .
ex:fetchWater        rdf:parameter1             ex:tool     .
ex:fetchWater        rdf:parameter2             ex:target_x     .
ex:fetchWater        rdf:parameter3             ex:target_y     .
ex:fetchWater        rdf:parameter4             ex:target_z     .
ex:thirsty        rdf:use             ex:drink     .
ex:drink        rdf:parameter1             ex:drinkType     .
ex:drink        rdf:parameter2             ex:speed     .
ex:move        rdf:parameter             ex:theta     .
ex:move        rdf:parameter             ex:phi     .
ex:move        rdf:parameter             ex:speed     .
}
"""
class AGENT():
    def __init__(self,name,energy=5.1):
        self.name = name
        '''
        知识图谱操作对象
        self.query(用于查询操作)
        self.update(更改，insert或者insert)
        '''
        self.query = SPARQLWrapper("http://localhost:3030/" + self.name + "/query")
        self.update = SPARQLWrapper("http://localhost:3030/" + self.name + "/update")
        self.query.setReturnFormat(JSON)
        self.update.setMethod('POST')
        # 创建初始知识
        self.getInitKnowledge()
        # 创建stm
        self.stm = STM(name,energy=energy)
        return
    """
#    getInitKnowledge方法
#    初始化agent知识
    """
    def getInitKnowledge(self):
        self.update.setQuery(knowledge)
        self.update.query()
        self.update.setQuery(
        "PREFIX rdf:   <http://www.w3.org/1999/02/22-rdf-syntax-ns#>"
        +"PREFIX ex:   <http://example.org/>"

        +"INSERT DATA {"
        +"ex:self        rdf:name             ex:" + self.name + "     ."
        +"}")
        self.update.query()
        return
    def __del__(self):
        return
#if __name__ == '__main__':
