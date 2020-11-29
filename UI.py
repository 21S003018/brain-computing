# -*- coding: utf-8 -*-
"""
Created on Wed Aug 14 20:01:38 2019

@author: C-82
"""
from builtin.agentFactory import AGENT

def make_people(name,args=5.1):
    '''
    开始运行一个agent
    :param name:
    :return:
    '''
    from multiprocessing import Process
    Process(target = AGENT,args = [name,args]).start()
if __name__ == "__main__":
    make_people('cbz')
    make_people('zsw',10)
