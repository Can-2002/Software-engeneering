import pandas as pd
def einlese_daten(dateipfad): 
     #Laden der CSV Datei und gibt einen Dataframe zurück

    try:
        df = pd.read_csv(dateipfad) 
        return df
    except FileNotFoundError:
        print(f"Datei unter {dateipfad} nicht gefunden!")
        return None