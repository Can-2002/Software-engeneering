# Datei: cleaning.py
# Zweck: Python Modul

# Dieses Modul enthält Funktionen zur Datenbereinigung.

# Imports für dieses Modul
import pandas as pd  # Import der pandas-Bibliothek für Datenverarbeitung

# Hier findet die Datenbereinigung statt
def datenbereinigung(df_rohdaten):
    # 1. Leerzeichen aus Spaltennamen entfernen
    df_rohdaten.columns = df_rohdaten.columns.str.strip()

    # 2. Spaltennamen ändern, um die Verarbeitung zu vereinfachen
    df_bereinigt = df_rohdaten.rename(columns={
        "MAC": "mac",
        "SSID": "ssid",
        "RSSI": "rssi",
        "CurrentLatitude": "lat",
        "CurrentLongitude": "lon",
        "FirstSeen": "timestamp"
    })

    # 3. Die Spalte mit Datum und Uhrzeit in ein Datumsformat konvertieren
    df_bereinigt["timestamp"] = pd.to_datetime(df_bereinigt["timestamp"])

    # 4. Leere Zeilen in den wichtigen Spalten löschen
    spalten_liste = ["mac", "ssid", "rssi", "lat", "lon", "timestamp"]
    df_bereinigt = df_bereinigt.dropna(subset=spalten_liste)
    return df_bereinigt  # Gibt den bereinigten DataFrame zurück