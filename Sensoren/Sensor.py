import sys
from queue import Queue
sys.path.insert(0, '../Handler/')
from DatabaseHandlers import MongoHandler
from collections import deque

class Sensor():

    def __init__(self,collection,queueDepth = 10):
        self.mongoHandler = MongoHandler()
        self.q = deque(maxlen=queueDepth)
        self.

    def addToQueue(self,obj):
        print("add element to queue:")
        print(obj)
        self.q.append(obj)

    def printQueue(self):
        print("clear and print queue:")
        for obj in self.q:
            print(obj)


