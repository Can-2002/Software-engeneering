import pandas as pd
#hier wird die Datenbereinigung stattfindne
def datenbereinigung(df_rohdaten):
    #1. Leerzeichen entfernen
    df_rohdaten.columns = df_rohdaten.columns.str.strip()
#2. Spaltennamnen ändern damit es schneller geht
    df_bereinigt = df_rohdaten.rename(columns={

        "MAC": "mac",
        "SSID": "ssid",
        "RSSI":"rssi",
        "CurrentLatitude":"lat",
        "CurrentLongitude": "lon",
        "FirstSeen": "timestamp"
    })
#3. Die spalte mit dem Datum und der Uhrzeit in ein Datumsformat ändern

    df_bereinigt["timestamp"] = pd.to_datetime(df_bereinigt["timestamp"])

#4. leere spalten löschen
    spalten_liste = ["mac","ssid","rssi","lat","lon","timestamp"]
    df_bereinigt = df_bereinigt.dropna(subset=spalten_liste)
    return df_bereinigt