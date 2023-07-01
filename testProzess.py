from multiprocessing import Process, Manager

class DataContainer:
    def __init__(self):
        self.data = {"name": "a", "value": 10}

    def get_value(self):
        return self.data["value"]

    def set_value(self, value):
        self.data["value"] = value

class TestServer(Process):
    def __init__(self, data_container):
        super().__init__()
        self.data_container = data_container

    def run(self):
        # Führe den Prozess aus und starte den Server
        self.start_server()

    def getDataA(self):
        return self.data_container.get().get_value()

    def setDataA(self, value):
        self.data_container.get().set_value(value)

    def start_server(self):
        # Hier kannst du deine Server-Initialisierung durchführen
        # Zum Beispiel ein Flask-Server, ein WebSocket-Server usw.
        # Du kannst hier auch andere Bibliotheken verwenden, die deinen Anforderungen entsprechen
        # Der Server sollte in einem eigenen Thread oder Prozess ausgeführt werden, um die parallele Ausführung zu ermöglichen
        pass

if __name__ == '__main__':
    with Manager() as manager:
        data_container = manager.Value("pkl", DataContainer())

        data_server = TestServer(data_container)
        data_server.start()

        # Beispielhafte Verwendung der Funktionen
        data = data_server.getDataA()
        print("Daten A:", data)

        data_server.setDataA(20)

        data = data_server.getDataA()
        print("Aktualisierte Daten A:", data)
