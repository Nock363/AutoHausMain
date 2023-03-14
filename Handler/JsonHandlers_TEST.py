from JsonHandlers import ConfigHandler 


configHandler = ConfigHandler()

configHandler.addActuator("TestEntry", "TestType", "TestCollection",0, {"Test1":1,"Test2":2})

configHandler.addSensor("TestEntry", 1, "TestClass",active=False)