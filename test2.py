# -*- coding: utf-8 -*-
"""
Created on Wed Aug 14 20:01:38 2019

@author: C-82
"""

#from SPARQLWrapper import SPARQLWrapper, JSON
#
## sparql = SPARQLWrapper("http://dbpedia.org/sparql")
#query = SPARQLWrapper("http://localhost:3030/cbz/query")
#update = SPARQLWrapper("http://localhost:3030/cbz/update")
#query.setReturnFormat(JSON)
#update.setMethod('POST')
#query.setQuery("""
#PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
#PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
#PREFIX ex: <http://example.org/>
#SELECT * WHERE {
#  ?sub rdf:use ?sssub
#}
#LIMIT 10
#""")
#update.setQuery(
#"PREFIX rdf:   <http://www.w3.org/1999/02/22-rdf-syntax-ns#>"
#+ "PREFIX rdfs:   <http://www.w3.org/2000/01/rdf-schema#>"
#+ "PREFIX ex:   <http://example.org/>"
#+ "PREFIX zoo:   <http://example.org/zoo/>"
#+ "PREFIX owl:   <http://www.w3.org/2002/07/owl#>"
#
#+ "DELETE DATA {"
#+ "ex:dog1    rdf:type         ex:animal ."
#+ "ex:cat1    rdf:type         ex:cat ."
#+ "ex:cat     rdfs:subClassOf  ex:animal ."
#+ "zoo:host   rdfs:range       ex:animal ."
#+ "ex:zoo1    zoo:host         ex:cat2 ."
#+ "ex:cat3    rdf:sameAs       ex:cat2 ."
#+ "}"
#        )
#
#update.query()
#ans = query.query().convert()
#print(ans['results']['bindings'])
'''
head -> vars
results -> bindings -> ? -> (type,value)
'''
#import globalvar as gl
#gl._init()
#gl.set_value('aa',1)
#for i in range(1000000000):
#    if i % 10000000 == 0:
#        print(gl.get_value('aa'))
#
#import os
#print(os.getcwd())
#import sys
#print(os.path.dirname(os.path.realpath(__file__)))
#import globalvar as gl
#def func():
#    gl._init()
#    gl.set_value('a',1)
#    return
#def func1():
#    print(gl.get_value('a'))
#    return
#if __name__ == '__main__':
##    import os
##    os.chdir(os.path.dirname(os.path.realpath(__file__)) + os.sep + "sourceAgent")
##    print(os.getcwd())
##    import stomach
##    from multiprocessing import Process
##    tmp = Process(target = func)
##    tmp.start()
##    while(True):
##        print(1)
#    from threading import Thread
#    tmp = Thread(target = func)
#    tmp.start()
#    tmp = Thread(target = func1)
#    tmp.start()



# string = '1111'
# string = string.replace('1','2')
# print(string)
# from lib.weightedKG import *
# G = graph('cbz')
# G.addEdge('mother','marriage','father')
# class ppp():
#     def __init__(self,name):
#         self.name = name
#         return
# P1 = ppp('cbz')
# lis = []
# lis.append(P1)
# lis2 = []
# lis2.append(P1)
# lis[0].name = 'bbb'
# print(lis[0].name)
# print(lis2[0].name)
import _thread
from threading import *

# def func():
#     while True:
#         import time
#         time.sleep(100000)
#     return
# thread = Thread(target = func)
# thread.join()
# import os
# print(os.path.dirname(os.path.realpath(__file__)))

# from IO import operate,over
# operate('go',[1,2])
import globalvar as gl
gl.set_value('bb',2)
import time
while True:
    print(gl.get_value('bb'))
    time.sleep(1)
