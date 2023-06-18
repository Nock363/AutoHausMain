from Utils.Container import MainContainer
from restAPI import RestAPI
from Scheduler import Scheduler


mainContainer = MainContainer()

scheduler = Scheduler(mainContainer=mainContainer)
restAPI = RestAPI(scheduler=Scheduler,mainContainer=mainContainer)
# restAPI.run()

scheduler.run()
# scheduler.startProcess()

print("init done")

#scheduler.runAllSensors()