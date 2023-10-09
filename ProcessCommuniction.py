from multiprocessing import Manager


class ProcessCommunication():

    def __init__(self):
        self.__manager = Manager()
        self.__reqChannel = self.__manager.list()
        self.__resChannel = self.__manager.list()
        self.__commandList = []

    #add commands. commands are names, a function and the needed arguments
    def addCommand(self, name, function, args):
        self.__commandList.append({"name": name, "function": function, "args": args})




#test to see if it works
if __name__ == "__main__":

    def testFunction1(test:int,name:str="Hello",alter:bool=True):
        print(f"{name}:{alter}")

    test = testFunction1.__annotations__

    processCommunication = ProcessCommunication()
    processCommunication.addCommand("test", print, ["test"])
