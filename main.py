from Utils.Container import MainContainer
from restAPI import RestAPI
from Scheduler import Scheduler
import time

mainContainer = MainContainer()

scheduler = Scheduler(mainContainer=mainContainer)
mainContainer.mainTestID = 55
# restAPI = RestAPI(scheduler=scheduler,mainContainer=mainContainer)
scheduler.startProcess()
# restAPI.run()
# scheduler.run()
#     
# while True:
#     scheduler.run()
#     print("running")

# # scheduler.run()

print("init done")

#scheduler.runAllSensors()