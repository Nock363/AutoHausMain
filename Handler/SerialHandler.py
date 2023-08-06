import serial.tools.list_ports
import time
import logging
logging.basicConfig(encoding='utf-8', level=logging.ERROR)



class SerialHandler:
    def __init__(self):
        self.esp_devices = []

    def find_esp8266_ports(self):
        esp_ports = []
        ports = list(serial.tools.list_ports.comports())
        for port in ports:
            if "USB2.0-Ser!" in port.description:
                esp_ports.append(port.device)
        return esp_ports

    def send_command(self, port, command, timeout=5):
        ser = serial.Serial(port, 19200, timeout=1)
        ser.write(command.encode())

        start_time = time.time()
        response = []

        lineRead = False
        while time.time() - start_time < timeout:
            if ser.in_waiting > 0:
                r = ser.readline().decode().strip()
                response.append(r)
                if len(response) > 0:  # Stop waiting if at least one response received
                    lineRead = True
            elif(lineRead == True):
                break
            time.sleep(0.1)  # Small delay to avoid excessive checking and CPU usage

        ser.close()
        end_time = time.time()

        print(f"Empfangszeit: {end_time - start_time:.2f} Sekunden")

        return response

        
    def update_esp_devices_status(self):
        for device in self.esp_devices:
            ser = serial.Serial(device['port'], 9600, timeout=1)
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
    serial_handler = SerialHandler()

    for i in range(0,10): 
        test = serial_handler.send_command(port="/dev/ttyUSB0",command="Status")
        print(test)
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
