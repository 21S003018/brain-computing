# -*- coding: utf-8 -*-

from queue import Queue, Empty
from threading import *


class EventManager:
    def __init__(self):
        self.__eventQueue = Queue()
        self.__active = False
        self.__thread = Thread(target = self.__Run)
        self.count = 0
        self.__handlers = {}

    def __Run(self):
        print('{}_run'.format(self.count))
        while self.__active == True:
            try:
                event = self.__eventQueue.get(block = True, timeout = 1)  
                self.__EventProcess(event)
            except Empty:
                pass
            self.count += 1

    def __EventProcess(self, event):
        print('{}_EventProcess'.format(self.count))
        if event.type_ in self.__handlers:
            for handler in self.__handlers[event.type_]:
                handler(event)
        self.count += 1

    def Start(self):
        print('{}_Start'.format(self.count))
        self.__active = True
        self.__thread.start()
        self.count += 1

    def Stop(self):
        print('{}_Stop'.format(self.count))
        self.__active = False
        self.__thread.join()
        self.count += 1

    def AddEventListener(self, type_, handler):
        print('{}_AddEventListener'.format(self.count))
        try:
            handlerList = self.__handlers[type_]
        except KeyError:
            handlerList = []
            self.__handlers[type_] = handlerList
        if handler not in handlerList:
            handlerList.append(handler)
        print(self.__handlers)
        self.count += 1

    def RemoveEventListener(self, type_, handler):
        print('{}_RemoveEventListener'.format(self.count))
        try:
            handlerList = self.__handlers[type_]
            if handler in handlerList:
                handlerList.remove(handler)
            if not handlerList:
                del self.__handlers[type_]
        except KeyError:
            pass
        self.count += 1

    def SendEvent(self, event):
        print('{}_SendEvent'.format(self.count))
        self.__eventQueue.put(event)
        self.count += 1


class Event:
    def __init__(self, type_=None):
        self.type_ = type_
        self.dict = {}
