import pandas as pd
import numpy as np


def rssi_zu_distanz(rssi, tx_power=-45, n=3.0):
    """
    Wandelt RSSI grob in eine Distanz um.
    tx_power = geschätzter RSSI bei 1 Meter
    n = Path-Loss-Exponent (Outdoor oft ca. 2.5 bis 3.5)
    """
    return 10 ** ((tx_power - rssi) / (10 * n))


def triangulation(df_datengefiltert):
    """
    Schätzt Routerpositionen auf Basis der Messpunkte.
    Berechnung pro MAC, Anzeige später nach SSID.
    """

    benoetigte_spalten = ["mac", "ssid", "lat", "lon", "rssi"]
    df = df_datengefiltert[benoetigte_spalten].copy()

    # Nur sinnvolle Zeilen behalten
    df = df.dropna(subset=["mac", "lat", "lon", "rssi"])

    router_liste = []

    for mac, gruppe in df.groupby("mac"):
        if len(gruppe) < 3:
            continue

        gruppe = gruppe.copy()

        # Distanz aus RSSI schätzen
        gruppe["distanz"] = gruppe["rssi"].apply(rssi_zu_distanz)

        # Gewicht: je kleiner die Distanz, desto höher das Gewicht
        gruppe["gewicht"] = 1 / (gruppe["distanz"] + 1e-6)

        # Geschätzte Position als gewichteter Mittelwert
        lat_router = np.average(gruppe["lat"], weights=gruppe["gewicht"])
        lon_router = np.average(gruppe["lon"], weights=gruppe["gewicht"])

        # Häufigste SSID dieser MAC
        ssid_router = gruppe["ssid"].mode().iloc[0] if gruppe["ssid"].notna().any() else "Unbekannt"

        router_liste.append({
            "mac": mac,
            "ssid": ssid_router,
            "router_lat": lat_router,
            "router_lon": lon_router,
            "messpunkte": len(gruppe),
            "mittleres_rssi": gruppe["rssi"].mean()
        })

    df_router_pos = pd.DataFrame(router_liste)
    return df_router_pos