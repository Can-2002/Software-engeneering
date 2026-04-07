import pandas as pd
import numpy as np


def rssi_zu_distanz(rssi, tx_power=-45, n=3.0):
    return 10 ** ((tx_power - rssi) / (10 * n))


def position_aus_routern_schaetzen(df_scan, df_router_pos):
    """
    Schätzt eine Nutzerposition aus einem Scan mit mehreren sichtbaren WLANs.
    df_scan: alle Messungen eines Zeitpunkts
    df_router_pos: geschätzte Routerpositionen
    """

    # Nur Router verwenden, die auch eine geschätzte Position haben
    df_merge = df_scan.merge(
        df_router_pos[["mac", "router_lat", "router_lon"]],
        on="mac",
        how="inner"
    )

    if len(df_merge) < 3:
        return None

    df_merge = df_merge.copy()
    df_merge["distanz"] = df_merge["rssi"].apply(rssi_zu_distanz)

    # Je kleiner die Distanz, desto höher das Gewicht
    df_merge["gewicht"] = 1 / (df_merge["distanz"] + 1e-6)

    lat = np.average(df_merge["router_lat"], weights=df_merge["gewicht"])
    lon = np.average(df_merge["router_lon"], weights=df_merge["gewicht"])

    return {
        "lat": lat,
        "lon": lon,
        "anzahl_router": len(df_merge)
    }


def route_schaetzen(df_datengefiltert, df_router_pos, scan_spalte="timestamp"):
    """
    Schätzt die gelaufene Route auf Basis der Routerpositionen.
    scan_spalte = Spalte, die einen Messzeitpunkt / Scan gruppiert
    """

    route_punkte = []

    for scan_id, gruppe in df_datengefiltert.groupby(scan_spalte):
        pos = position_aus_routern_schaetzen(gruppe, df_router_pos)

        if pos is None:
            continue

        route_punkte.append({
            scan_spalte: scan_id,
            "lat": pos["lat"],
            "lon": pos["lon"],
            "anzahl_router": pos["anzahl_router"]
        })

    df_route = pd.DataFrame(route_punkte)

    if not df_route.empty:
        df_route = df_route.sort_values(scan_spalte)

    return df_route