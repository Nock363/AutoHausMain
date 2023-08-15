import sqlite_utils

# Datenbankverbindung herstellen
db = sqlite_utils.Database("example.db")

# Beispiel-Daten
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

# Tabelle erstellen und Daten einfügen
table = db.table("my_table")
table.insert(data)

# Daten abrufen
result = table.rows_where('c__e__f = "f"')
for row in result:
    print(row)
