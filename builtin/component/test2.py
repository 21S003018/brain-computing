# import globalvar as gl
# # # gl._init()
# # # gl.set_value('name','cbz')
# # import time
# # time.sleep(7)
# # print(gl.get_value('name'))
# def func():
#     gl.environmentMessagePath = 'zkx'
#     return
# func()
import json
# import time
# while True:
#     file = open('1.txt', 'r')
#     print(file.readlines())
#     file.close()
from stmcache import SLOT

class test:
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
dic = {}
dic[1] = 2
print(dic.__contains__(1))