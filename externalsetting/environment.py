import json
import numpy as np
import time
from threading import Thread
import os
# 初始化数据
INIT_X = 0
INIT_Y = 0
PREDATOR_X = 112
PREDATOR_Y = 84
PREDATOR_R = 23
PREDATOR_V = 1
PREY_X = 100
PREY_Y = 100
AGENT_X = 88
AGENT_Y = 105
AGENT_R = 16
AGENTF_X = 88
AGENTF_Y = 110
AGENTF_R = 35
LIVE_DIS = 0.001

# 必要参数
environment_path = 'cbz/interaction/environmentMessage.json'
environment_path_f = 'zsw/interaction/environmentMessage.json'
control_path = 'cbz/interaction/agentControl.json'
control_path_f = 'zsw/interaction/agentControl.json'
environment = {}
environment['agent'] = {'x':AGENT_X,'y':AGENT_Y}
environment['agentf'] = {'x':AGENTF_X,'y':AGENTF_Y}
environment['prey'] = {'x':PREY_X,'y':PREY_Y}
environment['predator'] = {'x':PREDATOR_X,'y':PREDATOR_Y,'v':PREDATOR_V}
message = {}
message['hearing'] = {}
message['vision'] = {}

# 必要函数
def output(path,message):
    '''
    将字典写入文件
    :param path:
    :param message:
    :return:
    '''
    ans = str(json.dumps(message))
    file = open(path, 'w')
    file.write(ans)
    file.close()
    return
def read(path):
    '''
    从json文件中将数据读出来
    :param path:
    :return:
    '''
    file = open(path, 'r')
    message = json.load(file)
    file.close()
    return message
def broadcast(message):
    environment['hearing'] = message
    time.sleep(1)
    if environment.__contains__('hearing'):
        environment.pop('hearing')
    return

# lib函数
def distance(sub,obj):
    return np.sqrt((sub['x'] - obj['x'])**2 + (sub['y'] - obj['y'])**2)

def visiable():
    agent = environment['agent']
    agentf = environment['agentf']
    prey = environment['prey']
    predator = environment['predator']
    # print('agent',agent,'agentf',agentf,'prey',prey,'predator',predator)
    message['hearing'] = {}
    message['vision'] = {}
    if distance(agent,agentf) < AGENT_R:
        message['vision']['agentf'] = {}
        message['vision']['agentf']['x'] = agentf['x'] - agent['x']
        message['vision']['agentf']['y'] = agentf['y'] - agent['y']
    if distance(agent,prey) < AGENT_R:
        message['vision']['prey'] = {}
        message['vision']['prey']['x'] = prey['x'] - agent['x']
        message['vision']['prey']['y'] = prey['y'] - agent['y']
    if distance(agent,predator) < AGENT_R:
        message['vision']['predator'] = {}
        message['vision']['predator']['x'] = - agent['x'] + predator['x']
        message['vision']['predator']['y'] = - agent['y'] + predator['y']
    if environment.__contains__('hearing'):
        message['hearing'] = environment['hearing']
    return message

def visiablef():
    agent = environment['agent']
    agentf = environment['agentf']
    prey = environment['prey']
    predator = environment['predator']
    # print('agent',agent,'agentf',agentf,'prey',prey,'predator',predator)
    message['hearing'] = {}
    message['vision'] = {}
    if distance(agent,agentf) < AGENTF_R:
        message['vision']['agent'] = {}
        message['vision']['agent']['x'] = agent['x'] - agentf['x']
        message['vision']['agent']['y'] = agent['y'] - agentf['y']
    if distance(agentf,prey) < AGENTF_R:
        message['vision']['prey'] = {}
        message['vision']['prey']['x'] = prey['x'] - agentf['x']
        message['vision']['prey']['y'] = prey['y'] - agentf['y']
    if distance(agentf,predator) < AGENTF_R:
        message['vision']['predator'] = {}
        message['vision']['predator']['x'] = - agentf['x'] + predator['x']
        message['vision']['predator']['y'] = - agentf['y'] + predator['y']
    return message

def movedis(sub,obj):
    dis = distance(sub,obj)
    if dis < 0.001:
        return 0,0
    x = obj['x'] - sub['x']
    y = obj['y'] - sub['y']
    if dis < PREDATOR_V:
        return x,y
    return sub['v'] / dis * x, sub['v'] / dis * y

def note():
    global AGENT_R
    tmp = AGENT_R
    AGENT_R = 30
    time.sleep(5)
    AGENT_R = tmp
    return

def change():
    while True:
        agent = environment['agent']
        predator = environment['predator']
        if distance(predator, agent) < PREDATOR_R:
            x, y = movedis(predator, agent)
            environment['predator']['x'] += x
            environment['predator']['y'] += y
        output(environment_path_f, visiablef())
        output(environment_path, visiable())
        time.sleep(1)
        agent = environment['agent']
        agentf = environment['agentf']
        prey = environment['prey']
        predator = environment['predator']
        print('agent',agent,'agentf',agentf,'prey',prey,'predator',predator)
    return

def update():
    def parse(command):
        words = command.split('\t')
        method = words[0]
        params = words[1:]
        if method == 'go':
            x = float(params[0])
            y = float(params[1])
            environment['agent']['x'] += x
            environment['agent']['y'] += y
        elif method == 'eat':
            pass
        elif method == 'call':
            Thread(target=broadcast, args=(params[0],)).start()
        elif method == 'note':
            Thread(target=note).start()
        return
    last_mtime = os.stat(control_path).st_mtime
    while True:
        while last_mtime == os.stat(control_path).st_mtime:
            time.sleep(0.1)
        last_mtime = os.stat(control_path).st_mtime
        command = read(control_path)
        # print('command',command)
        operations = command['operation']
        for operation in operations:
            parse(operation)
        # print(visiable())
        agent = environment['agent']
        predator = environment['predator']
        if distance(agent,predator) < LIVE_DIS:
            print('agent die')
            break
        time.sleep(1)
    return

def updatef():
    def parse(command):
        words = command.split('\t')
        method = words[0]
        params = words[1:]
        if method == 'go':
            x = float(params[0])
            y = float(params[1])
            environment['agentf']['x'] += x
            environment['agentf']['y'] += y
        elif method == 'eat':
            pass
        elif method == 'call':
            Thread(target=broadcast, args=(params[0],)).start()
        elif method == 'note':
            Thread(target=note).start()
        return
    last_mtime = os.stat(control_path_f).st_mtime
    while True:
        while last_mtime == os.stat(control_path_f).st_mtime:
            time.sleep(0.1)
        last_mtime = os.stat(control_path_f).st_mtime
        command = read(control_path_f)
        print('agentf command',command)
        operations = command['operation']
        for operation in operations:
            parse(operation)
        agentf = environment['agentf']
        predator = environment['predator']
        # print(visiable())
        if distance(agentf,predator) < LIVE_DIS:
            print('agentf die')
            break
    return

if __name__ == '__main__':
    # update()
    # updatef()
    Thread(target=change).start()
    Thread(target=update).start()
    Thread(target=updatef).start()
    pass