from datetime import datetime


class Data():

    def __init__(self, data):
        self.__time = datetime.now()
        self.__data = data
    

    def __str__(self):
        return f"[{self.__time}] {self.__data}"

    @property
    def time(self):
        return self.__time

    @property
    def data(self):
        return self.__data
    
    def asPlainDict(self):
        retDict = self.__data.copy()
        retDict["time"] = self.__time
