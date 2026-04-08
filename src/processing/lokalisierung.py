# Datei: lokalisierung.py
# Zweck: Lokalisierung des Benutzers basierend auf WLAN-Signalstärken

# Imports für dieses Modul
import pandas as pd  # pandas wird für DataFrame-Verarbeitung verwendet
import numpy as np  # numpy wird für numerische Berechnungen verwendet


def rssi_zu_distanz(rssi, tx_power=-45, n=3.0):
    """Wandelt RSSI-Wert in eine ungefähre Distanz um.
    
    Parameter:
    - rssi: Der RSSI-Wert (Received Signal Strength Indicator) in dBm
    - tx_power: Geschätzter RSSI-Wert bei 1 Meter Entfernung (Standard: -45 dBm)
    - n: Path-Loss-Exponent für die Umgebung (Standard: 3.0, Indoor oft 2.5-3.5)
    
    Rückgabewert:
    - Distanz in Metern (geschätzt aus dem RSSI-Wert)
    """
    return 10 ** ((tx_power - rssi) / (10 * n))


def position_aus_routern_schaetzen(df_scan, df_router_pos):
    """Schätzt eine Nutzerposition aus einem WLAN-Scan mit mehreren sichtbaren Routern.
    
    Verwendet eine gewichtete Mittelwertbildung über alle sichtbaren Router,
    wobei nähere Router (basierend auf RSSI) höher gewichtet werden.
    
    Parameter:
    - df_scan: DataFrame mit allen WLAN-Messungen eines Zeitpunkts
    - df_router_pos: DataFrame mit geschätzten Routerpositionen
    
    Rückgabewert:
    - Dict mit keys 'lat', 'lon', 'anzahl_router' oder None wenn zu wenige Router
    """

    # Merge: Verbinde Messungen mit bekannten Routerpositionen
    df_merge = df_scan.merge(
        df_router_pos[["mac", "router_lat", "router_lon"]],
        on="mac",  # Vereinigung über MAC-Adresse
        how="inner"  # Nur Router mit bekannter Position
    )

    # Benötige mindestens 3 Router für eine sinnvolle Triangulation
    if len(df_merge) < 3:
        return None

    df_merge = df_merge.copy()
    # Berechne geschätzte Distanz für jeden Router basierend auf RSSI
    df_merge["distanz"] = df_merge["rssi"].apply(rssi_zu_distanz)

    # Gewichtung: Nähere Router (kleinere Distanz) bekommen höheres Gewicht
    # +1e-6 verhindert Division durch Null bei sehr kleinen Distanzen
    df_merge["gewicht"] = 1 / (df_merge["distanz"] + 1e-6)

    # Berechne gewichteten Mittelwert der Routerpositionen
    lat = np.average(df_merge["router_lat"], weights=df_merge["gewicht"])
    lon = np.average(df_merge["router_lon"], weights=df_merge["gewicht"])

    # Rückgabe der geschätzten Position und Anzahl genutzter Router
    return {
        "lat": lat,
        "lon": lon,
        "anzahl_router": len(df_merge)
    }


def route_schaetzen(df_datengefiltert, df_router_pos, scan_spalte="timestamp"):
    """Schätzt die gelaufene Route auf Basis der WLAN-Routerpositionen.
    
    Für jeden Scan (z.B. eine Zeitstelle) werden die Positionen aller sichtbaren
    Router trianguliert, um die geschätzte Position des Nutzers zu bestimmen.
    
    Parameter:
    - df_datengefiltert: Gefilterte Messdaten
    - df_router_pos: DataFrame mit geschätzten Routerpositionen
    - scan_spalte: Spaltenname für Scan-Gruppierung (Standard: 'timestamp')
    
    Rückgabewert:
    - DataFrame mit geschätzten Route-Punkten (lat, lon, anzahl_router)
    """

    route_punkte = []  # Liste zur Speicherung aller Route-Punkte

    # Gruppiere nach Scan-Zeitpunkt und bearbeite jeden Scan separat
    for scan_id, gruppe in df_datengefiltert.groupby(scan_spalte):
        # Schätze Position für diesen Scan-Zeitpunkt
        pos = position_aus_routern_schaetzen(gruppe, df_router_pos)

        # Überspringe Scan wenn keine Position geschätzt werden konnte
        if pos is None:
            continue

        # Füge Route-Punkt zur Liste hinzu
        route_punkte.append({
            scan_spalte: scan_id,  # Scan-Zeitpunkt
            "lat": pos["lat"],  # Geschätzte Breite
            "lon": pos["lon"],  # Geschätzte Länge
            "anzahl_router": pos["anzahl_router"]  # Anzahl genutzter Router
        })

    # Konvertiere Liste in DataFrame
    df_route = pd.DataFrame(route_punkte)

    # Sortiere nach Scan-Spalte (normalerweise chronologisch nach Zeitstempel)
    if not df_route.empty:
        df_route = df_route.sort_values(scan_spalte)

    return df_route