import pandas as pd
def einlese_daten(dateipfad): 
     #Laden der CSV Datei und gibt einen Dataframe zurück

    try:
        df_rohdaten = pd.read_csv(dateipfad, sep=",", skiprows=1) 
        return df_rohdaten
    except FileNotFoundError:
        print(f"Datei unter {dateipfad} nicht gefunden!")
        return None