from multiprocessing import Process
import os
from restAPI import RestAPI
from Scheduler import Scheduler
import time
from multiprocessing import Process, Event


scheduler = Scheduler()
restApi = RestAPI(scheduler=scheduler)



#starts the scheduler as a deamon which can be stopped by the restAPI
def startScheduler(flag):
    scheduler.runForever(flag)

#starts the restAPI as a deamon which can be stopped by the restAPI
def startRestApi():
    restApi.run()


# restApiProcess = Process(target=startRestApi)
# schedulerProcess.start()
#restApiProcess.start()


#stop all processes after 10 seconds    
#waits for the restAPI to finish
#restApiProcess.join()

restApi.run()