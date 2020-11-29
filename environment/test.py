import json
import numpy as np
import time
# 初始化数据
INIT_X = 0
INIT_Y = 0
PREDATOR_X = 0
PREDATOR_Y = 0
PREDATOR_R = 4
PREDATOR_V = 1
PREY_X = 0
PREY_Y = 0
AGENT_X = 1
AGENT_Y = 1
AGENT_R = 4
LIVE_DIS = 0.001

# 必要参数
environment_path = 'cbz/interaction/environmentMessage.json'
control_path = 'cbz/interaction/agentControl.json'
environment = {}
environment['agent'] = {'x':AGENT_X,'y':AGENT_Y}
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
    file = open(path, 'w')
    file.write(str(json.dumps(message)))
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

# lib函数
def distance(sub,obj):
    return np.sqrt((sub['x'] - obj['x'])**2 + (sub['y'] - obj['y'])**2)
def visiable():
    agent = environment['agent']
    prey = environment['prey']
    predator = environment['predator']
    print('agent',agent,'prey',prey,'predator',predator)
    if distance(agent,prey) < AGENT_R:
        message['vision']['prey'] = prey
    if distance(agent,predator) < AGENT_R:
        message['vision']['predator'] = predator
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
        return
    while True:
        command = read(control_path)
        print('command',command)
        operations = command['operation']
        for operation in operations:
            parse(operation)
        agent = environment['agent']
        predator = environment['predator']
        if distance(predator,agent) < PREDATOR_R:
            x,y = movedis(predator,agent)
            environment['predator']['x'] += x
            environment['predator']['y'] += y
        output(environment_path, visiable())
        if distance(agent,predator) < LIVE_DIS:
            print('die')
            break
        time.sleep(1)
    return

if __name__ == '__main__':
    update()
    pass