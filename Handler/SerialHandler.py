import serial.tools.list_ports
import time
import json
import logging
logging.basicConfig(encoding='utf-8', level=logging.ERROR)



class SerialHandler:
    def __init__(self):
        self.esp_devices = []
        self.__baudrate = 19200
        self.__ser = serial.Serial("/dev/ttyUSB0", self.__baudrate, timeout=1.0)
        time.sleep(2)

    def find_esp8266_ports(self):
        esp_ports = []
        ports = list(serial.tools.list_ports.comports())
        for port in ports:
            if "USB2.0-Ser!" in port.description:
                esp_ports.append(port.device)
        return esp_ports

    def send_command(self, port, command:dict, readResponse:bool=False, timeout=5):
        
        ser = serial.Serial("/dev/ttyUSB0", self.__baudrate, timeout=1.0)

        json_data = json.dumps(command)  # Daten als JSON-String serialisieren
        ser.write(json_data.encode())  # String in Bytes umwandeln und senden
        # qself.__ser.close()
        ser.close()

    def read_response(self, port, timeout=5.0):
        #ser = serial.Serial(port, self.__baudrate, timeout=1.0)
        
        #wait till response is available, but not longer than timeout
        start_time = time.time()
        while self.__ser.in_waiting == 0:
            if time.time() - start_time > timeout:
                logging.error(f"Timeout beim Warten auf Antwort von {port}")
                return None
        
        raw_response = self.__ser.readline().decode().strip()
        
        
        #create dict from json string. When response is not a valid json string, return None and log error
        try:
            response = json.loads(raw_response)
        except Exception as e:
            logging.error(f"Response von {port} ist kein gültiger JSON-String: {raw_response}")
            response = None

        #ser.close()
        return response
    

        
    def update_esp_devices_status(self):
        for device in self.esp_devices:
            ser = serial.Serial(device['port'], self.__baudrate, timeout=1)
            ser.write("Status".encode())
            time.sleep(0.1)
            if ser.in_waiting > 0:
                response = ser.readline().decode().strip()
                try:
                    if response:
                        parts = response.split(',')
                        name = parts[0].split(':')[1]
                        status = parts[1].split(':')[1]
                        device['status'] = status
                        device['name'] = name
                except Exception as e:
                    logging.error(f"Status für Gerät auf Port {device['port']} konnte nicht abgerufen werden.")
            else:
                logging.error(f"Keine Antwort erhalten von : {device['port']}") 

    def find_esp_devices(self):
        esp_ports = self.find_esp8266_ports()
        for port in esp_ports:
            device = {
                'port': port,
                'name': None,
                'status': None
            }
            self.esp_devices.append(device)

if __name__ == "__main__":
    serial_handler1 = SerialHandler()
    serial_handler2 = SerialHandler()

    #measure time for sending command and reading response
    start_time = time.time()
    #serial_handler2.send_command(port="/dev/ttyUSB0",command={"command":"setPump","pump":1,"runtime":1000})
    
    # serial_handler1.send_command(port="/dev/ttyUSB0",command={"command":"setPump","pump":1,"runtime":300})
    
    #print("start loop")

    serial_handler1.send_command(port="/dev/ttyUSB0",command={"command":"setPump","pump":2,"runtime":10000})
    
    serial_handler1.send_command(port="/dev/ttyUSB0",command={"command":"setPump","pump":1,"runtime":10000})
    #response2 = serial_handler1.read_response(port="/dev/ttyUSB0")
    serial_handler2.send_command(port="/dev/ttyUSB0",command={"command":"pumpStatus"})
    response1 = serial_handler1.read_response(port="/dev/ttyUSB0")    
    print("response1: ",response1)

    # for i in range(0,3):
    #     serial_handler1.send_command(port="/dev/ttyUSB0",command={"command":"setPump","pump":1,"runtime":100})
    #     print(f"run: {i}")
    #     # print("sleep first!")
    #     # time.sleep(5)
    #     print("now read response")
    #     response1 = serial_handler1.read_response(port="/dev/ttyUSB0")
    #     print("response1: ",response1)
    #     time.sleep(0.1)
        
    # serial_handler1.send_command(port="/dev/ttyUSB0",command={"command":"setPump","pump":2,"runtime":1000})
    

    # response2 = serial_handler2.read_response(port="/dev/ttyUSB0")
    
    # print("sleep")
    # time.sleep(3)
    print("done")
    # print(f"Time for sending command and reading response: {time.time() - start_time}")
    # print("response1: ",response1)
    # print("response2: ",response2)
    
    
    # serial_handler.find_esp_devices()
    # serial_handler.update_esp_devices_status()

    # print("Gefundene ESP-Geräte:")
    # for device in serial_handler.esp_devices:
    #     print(f"Port: {device['port']}, Name: {device['name']}, Status: {device['status']}")

    # Beispiel für das Senden des Befehls "Status" an ein Gerät mit dem Namen "my_esp_device"
    # response = serial_handler.send_command("my_esp_device", "Status")
    # if response:
    #     print("Antwort vom Gerät:")
    #     print(response)
    # else:
    #     print("Fehler beim Senden des Befehls oder Gerät nicht gefunden.")
