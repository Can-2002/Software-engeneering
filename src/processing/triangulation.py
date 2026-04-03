import pandas as pd
def triangulation(df_datengefiltert):

    n = 2
    a = -45
    df_berechnetedaten = df_datengefiltert[df_datengefiltert["rssi"]>=-85]

    df_berechnetedaten["distanz"] = 10 ** ((a - df_berechnetedaten["rssi"]) / (10 * n))

    return df_berechnetedaten
