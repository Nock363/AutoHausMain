from bluepy.btle import Peripheral, Scanner, DefaultDelegate, UUID, BTLEException, ADDR_TYPE_RANDOM
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
    while(True):
        try:
            peripheral = Peripheral(device_address)
            return peripheral
        except BTLEException as e:
            print("Verbindungsaufbau fehlgeschlagen")
            print(e)
            #time.sleep(2)

def createHexFromBytes(inputBytes):
    hex_representation = inputBytes.hex()
    return hex_representation   

# Adresse des Geräts, mit dem du dich verbinden möchtest
#device_address = "c0:00:00:01:9c:8e"        #Nr1
device_address = "c0:00:00:01:e8:b2"        #Nr2


# UUID der Charakteristik, von der du Daten lesen möchtest
# (Dies muss möglicherweise angepasst werden, basierend auf den Eigenschaften des Geräts)
characteristic_uuid = "0000ff01-0000-1000-8000-00805f9b34fb"        #Nr1
#characteristic_uuid = "0000ff01-0000-1000-8000-00805f9b34fb"        #Nr2

def printByteStream(byteStream):
    output = ""
    for b in byteStream:
        output = output + str(int(b)) + " "
    print(output)

def format_bytes(byte_stream):
    return ' '.join(format(byte, '08b') for byte in byte_stream)

def printByteStreamBinary(byteStream):

    binary_output = format_bytes(byteStream)
    print(binary_output)

def printByteStreamAsChar(byteStream):
    output = ""
    for b in byteStream:
        output = output + chr(b)
    print(output)

def reverse_bytes(bytes : list):
        return (bytes[0] << 8) + bytes[1]

def cutStream(data,mask):
    #example: mask = [1,4,7]
    cutStream = bytearray()
    for i in mask:
        cutStream.append(data[i])
    return cutStream
       

def decode_position(packet,idx):
    return reverse_bytes(packet[idx:idx+1])


def interpretBytes(byteStream):

    #PH Wert auslesen (byte 3 und 4)
    test = int(byteStream[16] << 8) + int(byteStream[17])


    #PH Wert auslesen (byte 3 und 4)
    ph_int = int(byteStream[3] << 8) + int(byteStream[4])
    ph = ph_int*0.01

    #EC Wert auslesen (byte 5 und 6)
    ec = int(byteStream[5] << 8) + int(byteStream[6])

    #PPM Wert auslesen (byte 7 und 8)
    ppm = int(byteStream[7] << 8) + int(byteStream[8])

    #mV Wert auslesen (byte 9 und 10)
    mv = int(byteStream[9] << 8) + int(byteStream[10])
    
    #Chlore Wert auslesen (byte 11 und 12)
    if(byteStream[11]== 0):
        chlore = int(byteStream[12])
    else:
        print("Chlore Wert out of Range")
        chlore=255 #TODO Muss gecatched werden
    
    #falls angabe in mS statt uS umrechnen: LSB von Byte 17.
    if(byteStream[17] & 0x01 == 1):
        ec = ec*1000
        


    #Temperatur auslesen (byte 13 und 14)
    temp = int(byteStream[13] << 8) + int(byteStream[14]) * 0.1


    output = {"test":test, "ph":ph,"ec":ec,"ppm":ppm,"mV":mv,"chlore":chlore, "temp":temp}
    print(output)
    return output


def deCode(pValue):
    pValue = bytearray(pValue)  # Convert to mutable bytearray
    len_pValue = len(pValue)

    for i in range(len_pValue - 1, 0, -1):
        tmp = pValue[i]
        hibit1 = (tmp & 0x55) << 1
        lobit1 = (tmp & 0xAA) >> 1
        tmp = pValue[i - 1]
        hibit = (tmp & 0x55) << 1
        lobit = (tmp & 0xAA) >> 1

        pValue[i] = (hibit1 | lobit)
        pValue[i - 1] = (hibit | lobit1)
    retValue = negateByteStream(bytes(pValue))
    return retValue  # Convert back to bytes before returning


def negateByteStream(byteStream):
    #negate bytes in byteStream
    negatedByteStream = bytearray()
    for b in byteStream:
        negB = ~b
        #cast negB as byte
        negB = negB & 0xFF
        negatedByteStream.append(negB)
    return negatedByteStream

try:
    # Verbinde dich mit dem Gerät
    print(f"Verbinde mit {device_address}")
    peripheral = connect_to_device(device_address)
    print("Verbindung aufgebaut")
    # Daten für 60 Sekunden auslesen
    timeout = 120  # Zeit in Sekunden
    start_time = time.time()
    dataLength  = -1
    changeMask = "X"
    lastData = None
    loopCounter = 0
    while time.time() - start_time < timeout:
        data = read_characteristic_data(peripheral, characteristic_uuid)
        # print(printByteStream(data))
        # print(f"raw data length: {len(data)}")
        
        #battery data test
        # battery = decode_position(data,15)
        # print(f"battery:{battery}")

        if(dataLength == -1):
            dataLength = len(data)
            #set changeMask to String
            changeMask = "X" * dataLength
            
            # print(f"inital changeMask: {changeMask}")
            lastData = data
        elif(dataLength != len(data)):
            raise(f"dataLength ist nicht passend zu bisherigen Laenge! dataLength: {dataLength} len(data)={len(data)}")


        #check if data changed and change corresponding X in changeMask to _
        for i in range(dataLength):
            if(lastData[i] != data[i]):
                changeMask = changeMask[:i] + "_" + changeMask[i+1:]
        lastData = data

        # print(f"[{loopCounter}]====================================")
        # print(f"data: {printByteStream(data)} | length: {dataLength}")
        # print(f"mask: {changeMask}")
        #data = cutStream()
        negData = negateByteStream(data)
        decodedData = deCode(data)
        # print("raw:")
        # printByteStreamBinary(data)
        #printByteStreamBinary(negData)
        # print("decoded:")
        printByteStreamBinary(decodedData)
        interpretBytes(decodedData)

        # print(" ")
        #print(f"first byte: {negData[0]}, second byte: {negData[1]}")
        # printByteStreamAsChar(data)
        # printByteStreamAsChar(negData)
        loopCounter = loopCounter+1

        # Warte 1 Sekunde, bevor die nächste Leseoperation erfolgt
        time.sleep(5)

    # Trenne die Verbindung zum Gerät
    peripheral.disconnect()
    print("Verbindung getrennt.")
except Exception as e:
    print(f"Fehler bei der Verbindung oder Datenabfrage: {e}")
