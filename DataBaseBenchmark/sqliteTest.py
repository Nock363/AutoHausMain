import sqlite3
import time
import random

# Verbindung zur Datenbank herstellen (wenn die Datenbank nicht vorhanden ist, wird sie erstellt)
conn = sqlite3.connect('main.db')

# Ein Cursor-Objekt erstellen, um die Datenbankabfragen auszuführen
cursor = conn.cursor()

# Tabelle "testTable" erstellen, wenn sie nicht existiert
cursor.execute('''
    CREATE TABLE IF NOT EXISTS testTable2 (
        id INTEGER PRIMARY KEY,
        time TIMESTAMP,
        data1 REAL,
        data2 REAL,
        data3 REAL
    )
''')

# 100 Datensätze in die Tabelle einfügen
for i in range(1, 101):
    current_time = time.time()
    data1 = random.uniform(0.0, 1.0)
    data2 = random.uniform(0.0, 1.0)
    data3 = random.uniform(0.0, 1.0)
    cursor.execute('INSERT INTO testTable2 (time, data1, data2, data3) VALUES (?, ?, ?, ?)',
                   (current_time, data1, data2, data3))

# Änderungen in der Datenbank speichern
conn.commit()

# Tabelle auslesen
cursor.execute('SELECT * FROM testTable2')
rows = cursor.fetchall()

# Ausgabe der Tabelleninhalte
for row in rows:
    print(row)

# Verbindung zur Datenbank beenden
conn.close()
