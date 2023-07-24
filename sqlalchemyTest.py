from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base

# Verbindung zur SQLite-Datenbank herstellen
engine = create_engine('sqlite:///Databases/main.db')

# Basisklasse für die Tabellendefinition erstellen
Base = declarative_base()

# Dictionary mit Tabellenname und Spaltendefinitionen
tabellen_definition = {
    "meine_tabelle": {
        "time": Float,
        "wert1": Integer,
        "wert2": String,
        "wert3": Boolean
    }
}

# Tabellenklasse dynamisch erstellen
for tabellenname, spaltendefinition in tabellen_definition.items():
    spalten = {
        '__tablename__': tabellenname,
        'id': Column(Integer, primary_key=True)
    }
    
    for spaltenname, spaltentyp in spaltendefinition.items():
        spalten[spaltenname] = Column(spaltenname, spaltentyp)
    
    # Klasse für die Tabelle erstellen
    Tabellenklasse = type(tabellenname.capitalize(), (Base,), spalten)
    
    # Tabelle in der Datenbank erstellen
    Base.metadata.create_all(engine)

print("Die Tabelle wurde erfolgreich erstellt.")
