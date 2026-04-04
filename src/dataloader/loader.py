# Datei: loader.py
# Zweck: Python Modul

# Dieses Modul enthält Funktionen zum Laden von Daten aus Dateien.

# Imports für dieses Modul
import pandas as pd  # Import der pandas-Bibliothek für Datenverarbeitung

# Funktion einlese_daten
def einlese_daten(dateipfad):
    # Lädt die CSV-Datei und gibt einen DataFrame zurück.
    # Überspringt die erste Zeile (Header), verwendet Komma als Separator.

    try:
        # Versucht, die CSV-Datei zu lesen
        df_rohdaten = pd.read_csv(dateipfad, sep=",", skiprows=1)
        return df_rohdaten  # Gibt den geladenen DataFrame zurück
    except FileNotFoundError:
        # Fehlerbehandlung: Falls die Datei nicht gefunden wird
        print(f"Datei unter {dateipfad} nicht gefunden!")
        return None  # Gibt None zurück bei Fehler