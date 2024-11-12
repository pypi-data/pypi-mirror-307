import json
from typing import Any, Optional

# Pfad zur JSON-Datei
JSON_FILE = "data.json"

# JSON-Datei laden oder erstellen
def load_data() -> dict:
    try:
        with open(JSON_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Daten in JSON-Datei speichern
def save_data(data: dict) -> None:
    with open(JSON_FILE, "w") as file:
        json.dump(data, file, indent=4)

# Daten erstellen oder aktualisieren
def create(key: str, value: Any) -> None:
    data = load_data()
    data[key] = value
    save_data(data)
    print(f'Daten hinzugefügt: {key} -> {value}')

# Daten lesen
def read(key: str) -> Optional[Any]:
    data = load_data()
    return data.get(key, "Eintrag nicht gefunden")

# Daten löschen
def delete(key: str) -> None:
    data = load_data()
    if key in data:
        del data[key]
        save_data(data)
        print(f'Daten gelöscht: {key}')
    else:
        print("Eintrag nicht gefunden")

# Alle Daten ausgeben (optional, falls du alle Daten sehen willst)
def read_all() -> dict:
    return load_data()
