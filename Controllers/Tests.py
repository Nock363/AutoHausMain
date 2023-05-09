from TimerController import TimerController


timer = TimerController({"from":"23:00:00","to":"23:50:00"})
result = timer.run()
print(result)