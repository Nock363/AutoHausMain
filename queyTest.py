from collections import deque

history = deque(maxlen=3)

def printQuey():
    #print queue in one line
    print(*history, sep=', ')

for i in range(10):
    history.append(i)
    printQuey()

