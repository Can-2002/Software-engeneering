# Dieses Skript lädt Daten aus einer CSV-Datei, bereinigt sie und zeigt die ersten Zeilen an.
# Es dient als Haupteinstiegspunkt für die Datenverarbeitung.

# Import der notwendigen Funktionen aus den Modulen
from dataloader.loader import einlese_daten  # Funktion zum Laden der Daten
from processing.cleaning import datenbereinigung  # Funktion zur Datenbereinigung
from processing.filtering import filter_data
def main():
    # Pfad zur CSV-Datei mit den Testdaten
    genutzte_csv = "/workspaces/Software-engeneering/data/Testdaten1.csv"

    # Laden der Rohdaten aus der CSV-Datei
    df_rohdaten = einlese_daten(genutzte_csv)

    # Bereinigung der geladenen Daten
    df_datenBereinigt = datenbereinigung(df_rohdaten)

    df_datenGefiltert = filter_data(df_datenBereinigt)
    print(len(df_datenGefiltert))


# Hauptprogramm: Führt die main-Funktion aus, wenn das Skript direkt ausgeführt wird
if __name__ == "__main__":
    main()









