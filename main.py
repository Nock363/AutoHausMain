import logging
import datetime

logFileName = "/home/user/AutoHausMain/Logs/System" + datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".log"

# Konfiguriere den Logger
logging.basicConfig(filename=logFileName, format="%(asctime)s [%(levelname)s]: %(message)s", level=logging.INFO)

# Erstelle einen Konsolen-Handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Füge den Konsolen-Handler zum Logger hinzu
logger = logging.getLogger()
logger.addHandler(console_handler)



class ErrorHandler(logging.Handler):
    def __init__(self, errorChannel,errorCount):
        logging.Handler.__init__(self)
        self.errorChannel = errorChannel
        self.errorCount = errorCount

    def emit(self, record):
        #check if the record is an error
        if record.levelno == logging.ERROR:
            #append record and time to the error channel as dict
            self.errorChannel.append({"time":datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S"),"record":record.msg})
            self.errorCount.value += 1


from restAPI import RestAPI
import time
from multiprocessing import Queue, Manager
import threading
from MainSystem import MainSystem
import sys

def errorLogTest():
    normalMode()
    print("trigger fake ERRORS:")
    logger.error("Test Log 1")
    logger.error("Test Log 2")
    logger.error("Test Log 3")
    logger.error("Test Log 4")

def brokenSensorTest():
    manager = Manager()
    reqChannel = manager.list()
    respChannel = manager.list()
    mainSystem = MainSystem(reqChannel=reqChannel,respChannel=respChannel)
    systemInfoBeforeTest = mainSystem.systemInfo()
    mainSystem.startBrokenSensor("Duengerautomat_Monitor")
    systemInfoAfterTest = mainSystem.systemInfo()
    print("done")

def test1():
    manager = Manager()
    reqChannel = manager.list()
    respChannel = manager.list()
    mainSystem = MainSystem(reqChannel=reqChannel,respChannel=respChannel)
    print(f"scheduler init: {mainSystem.statusScheduler()}")
    mainSystem.startScheduler()
    print(f"scheduler after 1st start: {mainSystem.statusScheduler()}")
    mainSystem.stopScheduler()
    time.sleep(20)
    print(f"scheduler after 1st stop: {mainSystem.statusScheduler()}")
    mainSystem.startScheduler()
    print(f"scheduler after 2st start: {mainSystem.statusScheduler()}")
    time.sleep(3)
    mainSystem.stopScheduler()
    print(f"scheduler after 2st stop: {mainSystem.statusScheduler()}")

def normalMode():
    #normal mode
    print("normal mode")
    manager = Manager()
    reqChannel = manager.list()
    respChannel = manager.list()
    errorChannel = manager.list()
    errorCount = manager.Value('i', 0)
    errorHandler = ErrorHandler(errorChannel,errorCount)
    logger.addHandler(errorHandler)


    mainSystem = MainSystem(reqChannel=reqChannel,respChannel=respChannel)
    restAPI = RestAPI(reqChannel=reqChannel,respChannel=respChannel,mainSystem=mainSystem,errorChannel=errorChannel,errorCount=errorCount)
    restAPI.run()
    mainSystem.setup()
    mainSystem.startScheduler()

#if as argument test is given then run test mode
if len(sys.argv) > 1 and sys.argv[1] == "test1":
    test1()
elif len(sys.argv) > 1 and sys.argv[1] == "brokenSensorTest":
    brokenSensorTest()
elif len(sys.argv) > 1 and sys.argv[1] == "errorLogTest":
    errorLogTest()
else:
    normalMode()

print("init done")
