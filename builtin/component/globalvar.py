# -*- coding: utf-8 -*-
"""
Created on Wed Aug 14 21:47:16 2019

@author: cbz
"""
globalvars = {}


def set_value(name,value):
    globalvars[name] = value
    return


def get_value(name):
    try:
        return globalvars[name]
    except:
        return None


def configpath(name):
    """
    配置交互文件路径
    :param name: agent的名字
    :return: None
    """
    import os
    root = os.path.realpath(__file__).replace('builtin\component\globalvar.py','')
    set_value('agentControlPath',os.path.join(root,'externalsetting/' + name + '/interaction/agentControl.json'))
    set_value('environmentMessagePath',os.path.join(root,'externalsetting/' + name + '/interaction/environmentMessage.json'))
    set_value('shortTimeKnowledgePath',os.path.join(root,'externalsetting/' + name + '/interaction/shortTimeKnowledge.json'))
    set_value('longTimeKnowledgePath',os.path.join(root,'externalsetting/' + name + '/interaction/longTimeKnowledge.json'))
    return
