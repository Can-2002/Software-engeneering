# Dieses Skript lädt Daten aus einer CSV-Datei, bereinigt sie und zeigt die ersten Zeilen an.
# Es dient als Haupteinstiegspunkt für die Datenverarbeitung.

# Import der notwendigen Funktionen aus den Modulen
from dataloader.loader import einlese_daten  # Funktion zum Laden der Daten
from processing.cleaning import datenbereinigung  # Funktion zur Datenbereinigung
from processing.filtering import filter_data
from visualization.map import map_erstellen
def main():
    # Pfad zur CSV-Datei mit den Testdaten
    genutzte_csv = "/workspaces/Software-engeneering/data/Testdaten1.csv"

    # Laden der Rohdaten aus der CSV-Datei
    df_rohdaten = einlese_daten(genutzte_csv)

    # Bereinigung der geladenen Daten
    df_datenBereinigt = datenbereinigung(df_rohdaten)

    df_datengefiltert = filter_data(df_datenBereinigt)
    
    map_print = map_erstellen(df_datengefiltert)


# Hauptprogramm: Führt die main-Funktion aus, wenn das Skript direkt ausgeführt wird
if __name__ == "__main__":
    main()









