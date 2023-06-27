from Utils.Container import MainContainer
import threading
import time

def run_sensor(sensor):
    dummySensor = sensor
    for _ in range(3):
        dummySensor.run()
        time.sleep(1)

def get_sensor_history(sensor):
    dummySensor = sensor
    for _ in range(3):
        history = dummySensor.run()
        time.sleep(2)

# Erstelle die Thread-Objekte
mainContainer = MainContainer()
dummy = mainContainer.getSensor("Dummy1")

thread1 = threading.Thread(target=run_sensor, args=(dummy,))
thread2 = threading.Thread(target=get_sensor_history, args=(dummy,))

# Starte die Threads
thread1.start()
thread2.start()

# Warte auf Beendigung der Threads
thread1.join()
thread2.join()

print("done")
