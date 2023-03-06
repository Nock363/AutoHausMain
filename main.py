from multiprocessing import Process
import os
from restAPI import RestAPI
from Scheduler import Scheduler
import time
import signal

restApi = RestAPI()
scheduler = Scheduler()


p_restApi = Process(target=restApi.run)
p_scheduler = Process(target=scheduler.runForever)

p_restApi.start()
p_scheduler.start()

#ask for user to input exit to stop the program
while True:
    if input() == "exit":
        p_restApi.terminate()
        p_scheduler.terminate()
        break
