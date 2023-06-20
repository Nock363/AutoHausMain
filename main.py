from Utils.Container import MainContainer
from restAPI import RestAPI
from Scheduler import Scheduler


mainContainer = MainContainer()

scheduler = Scheduler(mainContainer=mainContainer)
restAPI = RestAPI(scheduler=scheduler,mainContainer=mainContainer)
scheduler.startProcess()
restAPI.run()

# scheduler.run()

print("init done")

#scheduler.runAllSensors()