import pandas as pd
import numpy as np


def rssi_to_distance(rssi, tx_power=-45, n=3):
    """
    Wandelt RSSI in eine grobe Distanz (Meter) um
    """
    return 10 ** ((tx_power - rssi) / (10 * n))


def estimate_router_position(df_router):
    """
    Schätzt die Position eines einzelnen Routers
    """

    # RSSI -> Distanz
    distances = df_router["rssi"].apply(rssi_to_distance)

    # Gewicht berechnen (starke Signale wichtiger)
    weights = 1 / (distances + 1e-6)

    # gewichteter Mittelwert
    lat = np.average(df_router["lat"], weights=weights)
    lon = np.average(df_router["lon"], weights=weights)

    return lat, lon


def triangulation(df):
    """
    Berechnet die Position aller Router
    """

    router_positions = []

    # nach MAC gruppieren
    grouped = df.groupby("mac")

    for mac, group in grouped:

        # nur verwenden wenn genug Messpunkte
        if len(group) < 5:
            continue

        lat, lon = estimate_router_position(group)

        router_positions.append({
            "mac": mac,
            "lat": lat,
            "lon": lon,
            "messungen": len(group)
        })

    return pd.DataFrame(router_positions)