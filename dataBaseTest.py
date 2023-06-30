import sqlite3
# import time
from Handler.DatabaseHandlers import SqliteHandler


handler = SqliteHandler()

# time1 = time.time()
# result1 = handler.readData("Dummy1",100)
# time2 = time.time()

# print(f"time:{time2-time1}")

handler.addIndexToTable("Dummy1","time")

def get_table_indexes(connection, table_name):
    cursor = connection.cursor()
    cursor.execute(f"PRAGMA index_list({table_name})")
    indexes = cursor.fetchall()
    index_names = [index[1] for index in indexes]
    return index_names

# Verbindung zur Datenbank herstellen
conn = sqlite3.connect('Databases/main.db')

# Indexe für die Tabelle "Dummy1" abrufen
table_name = "Dummy1"
indexes = get_table_indexes(conn, table_name)

# Ausgabe der Indexe
if indexes:
    print(f"Die Tabelle '{table_name}' hat folgende Indexe:")
    for index in indexes:
        print(index)
else:
    print(f"Die Tabelle '{table_name}' hat keine Indexe.")

# Verbindung schließen
conn.close()