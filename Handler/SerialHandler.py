import serial.tools.list_ports
import time
import json
import logging
logging.basicConfig(encoding='utf-8', level=logging.ERROR)



class SerialHandler:
    def __init__(self,baudrate = 19200):
        self.__baudrate = baudrate
        self.devices = self.__find_devices()
        
        

    def __send_command(self, port, command:dict,timeout=1.0):
        
        ser = serial.Serial(port, self.__baudrate, timeout=timeout)
        json_data = json.dumps(command)  # Daten als JSON-String serialisieren
        ser.write(json_data.encode())  # String in Bytes umwandeln und senden
        # qself.__ser.close()
        ser.close()

    def __read_response(self, port, timeout=1.0):
        ser = serial.Serial(port, self.__baudrate, timeout=timeout)
        #wait till response is available, but not longer than timeout
        start_time = time.time()
        while ser.in_waiting == 0:
            if time.time() - start_time > timeout:
                logging.error(f"Timeout beim Warten auf Antwort von {port}. Prüfe ob eine überhaupt eine Antwort erwartet wird.")
                return None
        
        raw_response = ser.readline().decode().strip()
        ser.close()
        
        #create dict from json string. When response is not a valid json string, return None and log error
        try:
            response = json.loads(raw_response)
        except Exception as e:
            logging.error(f"Response von {port} ist kein gültiger JSON-String: {raw_response}")
            response = None

        #ser.close()
        return response

    def __find_devices(self):
        
        devices = []
        ports = list(serial.tools.list_ports.comports())
        for port in ports:
            if "USB2.0-Ser!" in port.description or "USB Serial" in port.description:
                #ESP D1 Minis werden so erkannt
                device = {
                    'port': port.device,
                    'raw': port, 
                    'name': None,
                    'status': None
                }
                devices.append(device)
            else:
                #weitere Systeme können ergänzt werden
                pass
        
        for device in devices:
            self.__send_command(device['port'],{"command":"info"})
            response = self.__read_response(device['port'])
            device['name'] = response['name']
            print(f"Serial Gerät gefunden: {device['name']}")


        return devices

    
    def check_for_device(self,deviceName:str):
        for device in self.devices:
            if device['name'] == deviceName:
                return True
        return False

    def send_dict(self,deviceName:str,command:dict,readResponse:bool=False):

        #find device with given name
        device = None
        for d in self.devices:
            if d['name'] == deviceName:
                device = d
                break
        
        if device is None:
            raise Exception(f"Device mit dem Namen {deviceName} nicht gefunden.")
        
        #send command
        self.__send_command(device['port'],command)

        #read response if requested
        if readResponse:
            response = self.__read_response(device['port'])
            return response
        else:
            return None


if __name__ == "__main__":
    serial_handler1 = SerialHandler()
    deivceIsThere = serial_handler1.check_for_device("Düngeranlage")
    result = serial_handler1.send_dict("Düngeranlage",{"command":"setPump","pump":1,"runtime":1000},readResponse=True)
    print(result)

    print("done")