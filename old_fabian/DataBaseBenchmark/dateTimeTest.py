import sqlite3
from datetime import datetime

# Verbindung zur SQLite-Datenbank herstellen
conn = sqlite3.connect('datenbank.db')
cursor = conn.cursor()

# CREATE TABLE-Anweisung ausführen, falls die Tabelle nicht existiert
cursor.execute('''CREATE TABLE IF NOT EXISTS meine_tabelle (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    datum_spalte DATETIME)''')

# DateTime-Wert erstellen
now = datetime.now()

# query = 
# DateTime-Wert in die Datenbank einfügen
cursor.execute("INSERT INTO meine_tabelle (datum_spalte) VALUES (?)", (now,))

# Änderungen bestätigen und Verbindung schließen
conn.commit()
conn.close()
