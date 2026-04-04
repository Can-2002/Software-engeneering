# Datei: filtering.py
# Zweck: Python Modul

# Imports für dieses Modul
import pandas as pd  # pandas wird für DataFrame-Verarbeitung verwendet


# Funktion filter_data
def filter_data(df_datenBereinigt):
    """Filtert den DataFrame so, dass nur MAC-Adressen mit mindestens 3 Messpunkten erhalten bleiben."""
    # Zähle, wie oft jede MAC-Adresse vorkommt
    counts = df_datenBereinigt["mac"].value_counts()

    # Behalte nur Einträge mit mindestens 3 Vorkommen
    df_gefiltert = df_datenBereinigt[df_datenBereinigt["mac"].isin(counts[counts >= 3].index)]

    # Gebe den gefilterten DataFrame zurück
    return df_gefiltert

