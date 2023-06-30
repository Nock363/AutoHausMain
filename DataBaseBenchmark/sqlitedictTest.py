from sqlitedict import SqliteDict

# Eine neue Datenbank erstellen oder eine vorhandene öffnen
my_dict = SqliteDict('my_database.db', autocommit=True)

# Daten hinzufügen 100 Mal
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

for i in range(100):
    key = f'testTable{i+1}'
    my_dict[key] = data

# Datenbank schließen
my_dict.close()
