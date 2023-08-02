from Utils.Container import MainContainer
from restAPI import RestAPI
from Scheduler import Scheduler
import time
from multiprocessing import Queue
import threading
from MainSystem import MainSystem

reqQueue = Queue()
respQueue = Queue()

mainSystem = MainSystem(reqQueue,respQueue)

# mainContainer = MainContainer(reqQueue,respQueue)
# scheduler = Scheduler(mainContainer=mainContainer)
restAPI = RestAPI(reqQueue=reqQueue, respQueue=respQueue,mainSystem=mainSystem)
mainSystem.startProcess()
multiProcessInterfaceThread = threading.Thread(target=mainSystem.startQueueWork)
multiProcessInterfaceThread.start()

# scheduler.run()
# scheduler.run()
# scheduler.run()

restAPI.run()




#     66
# while True:
#     scheduler.run()sdsmdnsm
#     print("running")

# # scheduler.run()

print("init done")

#scheduler.runAllSensors()