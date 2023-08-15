from restAPI import RestAPI
import time
from multiprocessing import Queue
import threading
from MainSystem import MainSystem

reqQueue = Queue()
respQueue = Queue()

mainSystem = MainSystem(reqQueue,respQueue)

restAPI = RestAPI(reqQueue=reqQueue, respQueue=respQueue,mainSystem=mainSystem)
# mainSystem.runNtimes(N=1)
mainSystem.startProcess()
# multiProcessInterfaceThread = threading.Thread(target=mainSystem.startQueueWork)
# multiProcessInterfaceThread.start()

# # time.sleep(20)
# print("start RestAPI")
restAPI.run()




#     66
# while True:
#     scheduler.run()sdsmdnsm
#     print("running")

# # scheduler.run()

print("init done")


#scheduler.runAllSensors()