import multiprocessing
import time
import logging

from schedulerTestProgramm import Test
logging.basicConfig(encoding='utf-8', level=logging.DEBUG)

def threadRunner(obj):
    obj.run()

tests = []
processes = []
processesCount = 100;
sleepTime = 1
for i in range(0,processesCount):
        test = Test(0.25,f"Ich bin test ({i})")
        process = multiprocessing.Process(target=threadRunner,args=(test,))
        tests.append(test)
        processes.append(process)


# test1 = Test(1,"Ich bin test1")
# test2 = Test(1,"Ich bin test2")

# thread1 = multiprocessing.Process(target=threadRunner,args=(test1,))
# thread2 = multiprocessing.Process(target=threadRunner,args=(test2,))

# processes.append(thread1)
# processes.append(thread2)
for p in processes:
        p.start()

time.sleep(10)
for p in processes:
        p.terminate()

