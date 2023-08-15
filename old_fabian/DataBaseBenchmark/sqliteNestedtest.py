import sqlite3

# Daten definieren
data = {
    'a': 1,
    'b': 2,
    'c': {
        'd': 3,
        'e': {
            'f': 4,
            'g': 5
        }
    }
}

# Funktion zum Erstellen der Tabelle
def create_table(conn):
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS my_table
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, key TEXT, value TEXT)''')
    conn.commit()

# Funktion zum Speichern der Daten
def save_data(conn, data, parent_key=''):
    cursor = conn.cursor()
    for key, value in data.items():
        if isinstance(value, dict):
            save_data(conn, value, parent_key + key + '/')
        else:
            cursor.execute("INSERT INTO my_table (key, value) VALUES (?, ?)",
                           (parent_key + key, str(value)))
    conn.commit()

# Funktion zum Laden der Daten
def load_data(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT key, value FROM my_table")
    rows = cursor.fetchall()
    data = {}
    for row in rows:
        keys = row[0].split('/')
        value = row[1]
        current_dict = data
        for key in keys[:-1]:
            if key not in current_dict:
                current_dict[key] = {}
            current_dict = current_dict[key]
        current_dict[keys[-1]] = eval(value)
    return data

# SQLite-Verbindung herstellen
conn = sqlite3.connect('nestTest.db')

# Tabelle erstellen
create_table(conn)

# Daten speichern
save_data(conn, data)

# Daten laden
loaded_data = load_data(conn)

# Verbindung schließen
conn.close()

# Daten ausgeben
print(loaded_data)
