from pymongo import MongoClient
import time
import matplotlib.pyplot as plt

# Verbindung zur MongoDB herstellen
client = MongoClient('mongodb://localhost:27017/')

# Datenbank und Sammlung auswählen
db = client['main']

collection_name = 'mongoBenchmark' + time.strftime('%m_%d_%H_%M_%S')
collection = db[collection_name]

# Anzahl der Durchläufe und Anfangsgröße der Sammlung festlegen
num_runs = 100
documents_to_add = 5000
base_size = 0

# Listen zur Speicherung der Ergebnisse
last_size = 0
collection_sizes = []
average_read_times = []
average_write_times = []


# Indexierung für das Feld 'time' erstellen
collection.create_index([('time', -1)])

#create a fake time to 12:00:00
fakeTime = time.time()
def write_data(lenght):
    #adds data as batch to collection
    global fakeTime
    documents = []
    for i in range(lenght):
        document = {'name': f'Dokument {i}', 'time': fakeTime}
        fakeTime = fakeTime + 1
        documents.append(document)
    time1 = time.time()
    collection.insert_many(documents)
    return time.time() - time1


def read_data(lenght):
    #read lenght documents from collection. read the newest documents by time
    time1 = time.time()
    result = list(collection.find().sort('time', -1).limit(lenght))
    return time.time() - time1


# #fill collection with data before benchmarking
# print(f"Erstelle Sammlung mit {base_size} Dokumenten")
# baseTime = write_data(base_size)
# print(f"Erstellt in {baseTime} Sekunden")

print("first sleep for 10 seconds")
time.sleep(10)

print("size;write;read")
for i in range(num_runs):
    
    writeTime = write_data(documents_to_add)
    readTime = read_data(documents_to_add)
    average_write_times.append(writeTime)
    average_read_times.append(readTime)
    last_size = last_size + documents_to_add
    collection_sizes.append(last_size)
    print(f"{last_size};{writeTime};{readTime}")

# Verbindung schließen
client.close()

writeImage = 'write_time' + time.strftime('%m_%d_%H_%M_%S') + '.png'
readImage = 'read_time' + time.strftime('%m_%d_%H_%M_%S') + '.png'

# Ergebnisse plotten als zwei einzelne plots
plt.plot(collection_sizes, average_write_times, label='Schreibzeit')
plt.xlabel('Anzahl der Dokumente')
plt.ylabel('Zeit in Sekunden')
plt.title('Schreibzeit')
plt.legend()
plt.savefig(writeImage)
plt.clf()

plt.plot(collection_sizes, average_read_times, label='Lesezeit')
plt.xlabel('Anzahl der Dokumente')
plt.ylabel('Zeit in Sekunden')
plt.title('Lesezeit')
plt.legend()
plt.savefig(readImage)
plt.clf()

print("Plots gespeichert als:")
print(writeImage)
print(readImage)