import sqlite3
import time
import matplotlib.pyplot as plt

# Verbindung zur SQLite-Datenbank herstellen (wenn die Datenbank nicht vorhanden ist, wird sie erstellt)
conn = sqlite3.connect('main.db')

# Ein Cursor-Objekt erstellen, um die Datenbankabfragen auszuführen
cursor = conn.cursor()

# Tabelle für den Benchmark erstellen, wenn sie nicht existiert
cursor.execute('''
    CREATE TABLE IF NOT EXISTS sqliteBenchmark2 (
        id INTEGER PRIMARY KEY,
        name TEXT,
        time TIMESTAMP
    )
''')

cursor.execute('CREATE INDEX IF NOT EXISTS time_index ON sqliteBenchmark2 (time)')


# Anzahl der Durchläufe und Anfangsgröße der Tabelle festlegen
num_runs = 100
rows_to_add = 5000
base_size = 0

# Listen zur Speicherung der Ergebnisse
last_size = 0
table_sizes = []
average_read_times = []
average_write_times = []

# Fake-Zeit erstellen
fake_time = time.time()

def write_data(length):
    # Daten als Batch in die Tabelle einfügen
    global fake_time
    values = []
    for i in range(length):
        values.append((f'Dokument {i}', fake_time))
        fake_time += 1
    time1 = time.time()
    cursor.executemany('INSERT INTO sqliteBenchmark2 (name, time) VALUES (?, ?)', values)
    conn.commit()
    return time.time() - time1

def read_data(length):
    # Lese length Dokumente aus der Tabelle, sortiert nach Zeit
    time1 = time.time()
    cursor.execute('SELECT * FROM sqliteBenchmark2 ORDER BY time DESC LIMIT ?', (length,))
    result = cursor.fetchall()
    return time.time() - time1

# Vor dem Benchmark Daten in die Tabelle einfügen
# print(f"Erstelle Tabelle mit {base_size} Dokumenten")
# base_time = write_data(base_size)
# print(f"Erstellt in {base_time} Sekunden")

print("Warte 10 Sekunden")
#time.sleep(10)

print("Größe;Schreiben;Lesen")
for i in range(num_runs):
    write_time = write_data(rows_to_add)
    read_time = read_data(rows_to_add)
    average_write_times.append(write_time)
    average_read_times.append(read_time)
    last_size += rows_to_add
    table_sizes.append(last_size)
    print(f"{last_size};{write_time};{read_time}")

# Verbindung zur Datenbank schließen
conn.close()

write_image = 'write_timeSQLite' + time.strftime('%m_%d_%H_%M_%S') + '.png'
read_image = 'read_timeSQLite' + time.strftime('%m_%d_%H_%M_%S') + '.png'

# Ergebnisse als separate Plots anzeigen
plt.plot(table_sizes, average_write_times, label='Schreibzeit')
plt.xlabel('Anzahl der Dokumente')
plt.ylabel('Zeit in Sekunden')
plt.title('Schreibzeit')
plt.legend()
plt.savefig(write_image)
plt.clf()

plt.plot(table_sizes, average_read_times, label='Lesezeit')
plt.xlabel('Anzahl der Dokumente')
plt.ylabel('Zeit in Sekunden')
plt.title('Lesezeit')
plt.legend()
plt.savefig(read_image)
plt.clf()

print("Plots gespeichert als:")
print(write_image)
print(read_image)
