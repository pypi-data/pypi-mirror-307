import tkinter as tk
from tkinter import filedialog
import re


def get_imports(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    imports = []
    # Regex für "import x" und "from x import y"
    import_pattern = re.compile(r"^\s*import\s+(\S+)")
    from_import_pattern = re.compile(r"^\s*from\s+(\S+)\s+import\s+(\S+)")

    for line in lines:
        # Nach einfachen Imports suchen
        match_import = import_pattern.match(line)
        if match_import:
            imports.append(match_import.group(1).split('.')[0])

        # Nach "from ... import ..." suchen
        match_from_import = from_import_pattern.match(line)
        if match_from_import:
            module = match_from_import.group(1).split('.')[0]
            imports.append(module)

    # Entferne doppelte Einträge
    imports = sorted(set(imports))

    # Falls keine Imports gefunden wurden, "nomods" zurückgeben
    if not imports:
        return "nomods"

    # Formatiere als "package1", "package2", "package3"
    formatted_imports = ', '.join(f'"{imp}"' for imp in imports)
    return formatted_imports


def writenewline(filename, texttowrite):
    """
    Schreibt den angegebenen Text als neue Zeile in die Datei.

    :param filename: Name der Datei, in die geschrieben werden soll.
    :param texttowrite: Der Text, der als neue Zeile geschrieben werden soll.
    """
    with open(filename, 'a') as file:  # 'a' steht für 'append', um an die Datei anzuhängen
        file.write(texttowrite + '\n')

def choose_file():
    root = tk.Tk()
    root.withdraw()  # Versteckt das Hauptfenster
    file_path = filedialog.askopenfilename()  # Öffnet das Dateiauswahlfenster
    return file_path

def getcoms(filename):
    # Liste zum Speichern der gefundenen Funktionen
    functions = []
    
    # Datei einlesen
    with open(filename, "r") as file:
        lines = file.readlines()
    
    # Durch alle Zeilen iterieren
    for line in lines:
        line = line.strip()  # Entfernt führende und nachfolgende Leerzeichen
        
        # Prüfen, ob die Zeile mit "def " beginnt
        if line.startswith("def "):
            # Funktionsnamen extrahieren (zwischen "def " und "(")
            func_name = line[4:line.index("(")].strip()
            functions.append(func_name)
    
    return functions

    
def writetofile(filename, texttowrite):
    
    with open(filename, 'a') as file:  # 'a' steht für 'append', um an die Datei anzuhängen
        file.write(texttowrite)