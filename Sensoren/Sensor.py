import sys
from queue import Queue
sys.path.insert(0, '../Handler/')
from DatabaseHandlers import MongoHandler
from collections import deque
import logging

logging.basicConfig(encoding='utf-8', level=logging.DEBUG)

class Sensor():

    def __init__(self,collection,pinID,queueDepth = 10):
        self.mongoHandler = MongoHandler()
        pin = self.mongoHandler.getPin(pinID)
        self.q = deque(maxlen=queueDepth)
        

    def addToQueue(self,obj):
        print("add element to queue:")
        print(obj)
        self.q.append(obj)

    def printQueue(self):
        print("clear and print queue:")
        for obj in self.q:
            print(obj)


