from bluepy.btle import Peripheral, Scanner, DefaultDelegate, UUID
import time

# Funktion zum Lesen der Daten aus einer Charakteristik
def read_characteristic_data(peripheral, characteristic_uuid):
    service_uuid = UUID(characteristic_uuid)
    service = peripheral.getServiceByUUID(service_uuid)
    characteristic = service.getCharacteristics()[0]
    data = characteristic.read()
    return data

# Funktion zum Scannen und Verbinden mit dem Gerät
def connect_to_device(device_address):
    peripheral = Peripheral(device_address)
    return peripheral

def createHexFromBytes(inputBytes):
    hex_representation = inputBytes.hex()
    return hex_representation   

# Adresse des Geräts, mit dem du dich verbinden möchtest
device_address = "c0:00:00:01:9c:8e"

# UUID der Charakteristik, von der du Daten lesen möchtest
# (Dies muss möglicherweise angepasst werden, basierend auf den Eigenschaften des Geräts)
characteristic_uuid = "0000ff01-0000-1000-8000-00805f9b34fb"

def printByteStream(byteStream):
    output = ""
    for b in byteStream:
        output = output + str(int(b)) + " "
    print(output)


def reverse_bytes(bytes : list):

        return (bytes[0] << 8) + bytes[1]

       

def decode_position(packet,idx):

    return reverse_bytes(packet[idx:idx+2])


try:
    # Verbinde dich mit dem Gerät
    print(f"Verbinde mit {device_address}")
    peripheral = connect_to_device(device_address)
    print("Verbindung aufgebaut")
    # Daten für 60 Sekunden auslesen
    timeout = 60  # Zeit in Sekunden
    start_time = time.time()
    dataLength  = -1
    changeMask = "X"
    lastData = None
    loopCounter = 0
    while time.time() - start_time < timeout:
        data = read_characteristic_data(peripheral, characteristic_uuid)
        print(printByteStream(data))
        print(f"raw data length: {len(data)}")
        hexData = createHexFromBytes(data)

        #battery data test
        # battery = decode_position(data,15)
        # print(f"battery:{battery}")

        if(dataLength == -1):
            dataLength = len(hexData)
            #set changeMask to String
            changeMask = "X" * dataLength
            print(f"inital changeMask: {changeMask}")
            lastData = hexData
        elif(dataLength != len(hexData)):
            raise(f"dataLength ist nicht passend zu bisherigen Laenge! dataLength: {dataLength} len(hexData)={len(hexData)}")


        #check if data changed and change corresponding X in changeMask to _
        for i in range(dataLength):
            if(lastData[i] != hexData[i]):
                changeMask = changeMask[:i] + "_" + changeMask[i+1:]
        lastData = hexData

        print(f"[{loopCounter}]====================================")
        print(f"data: {hexData} | length: {dataLength}")
        print(f"mask: {changeMask}")
        

        loopCounter = loopCounter+1

        # Warte 1 Sekunde, bevor die nächste Leseoperation erfolgt
        time.sleep(1.5)

    # Trenne die Verbindung zum Gerät
    peripheral.disconnect()
    print("Verbindung getrennt.")
except Exception as e:
    print(f"Fehler bei der Verbindung oder Datenabfrage: {e}")
