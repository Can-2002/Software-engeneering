# Datei: triangulation.py
# Zweck: Triangulation zur Schätzung von Router-Positionen

# Imports für dieses Modul
import pandas as pd  # pandas wird für DataFrame-Verarbeitung verwendet
import numpy as np  # numpy wird für numerische Berechnungen verwendet


def rssi_zu_distanz(rssi, tx_power=-45, n=3.0):
    """Wandelt RSSI-Wert in eine ungefähre Distanz um.
    
    Nutzt das Free Space Path Loss Modell für die Umrechnung.
    
    Parameter:
    - rssi: Der RSSI-Wert (Received Signal Strength Indicator) in dBm
    - tx_power: Geschätzter RSSI-Wert bei 1 Meter Entfernung (Standard: -45 dBm)
    - n: Path-Loss-Exponent (Standard: 3.0, Outdoor oft 2.5-3.5)
    
    Rückgabewert:
    - Distanz in Metern (geschätzt)
    """
    return 10 ** ((tx_power - rssi) / (10 * n))


def triangulation(df_datengefiltert):
    """Schätzt Routerpositionen durch Triangulation basierend auf WLAN-Messpunkten.
    
    Für jeden Router (identifiziert durch MAC-Adresse) werden die Messungen
    analysiert, und basierend auf den RSSI-Werten und GPS-Koordinaten der
    Messorte wird eine geschätzte Router-Position berechnet.
    
    Parameter:
    - df_datengefiltert: DataFrame mit gefilterten Messdaten
    
    Rückgabewert:
    - DataFrame mit geschätzten Router-Positionen und Statistiken
    """

    # Wähle nur benötigte Spalten aus
    benoetigte_spalten = ["mac", "ssid", "lat", "lon", "rssi"]
    df = df_datengefiltert[benoetigte_spalten].copy()

    # Entferne Zeilen mit fehlenden Daten
    df = df.dropna(subset=["mac", "lat", "lon", "rssi"])

    router_liste = []  # Speichert die geschätzten Router-Positionen

    # Verarbeite jeden Router (MAC-Adresse) separat
    for mac, gruppe in df.groupby("mac"):
        # Benötige mindestens 3 Messpunkte für eine sinnvolle Triangulation
        if len(gruppe) < 3:
            continue

        gruppe = gruppe.copy()

        # Berechne geschätzte Distanz für jeden Messpunkt basierend auf RSSI
        gruppe["distanz"] = gruppe["rssi"].apply(rssi_zu_distanz)

        # Berechne Gewichte: Näher gelegene Messpunkte bekommen höhere Gewichte
        # (+1e-6 verhindert Division durch Null)
        gruppe["gewicht"] = 1 / (gruppe["distanz"] + 1e-6)

        # Schätze Router-Position als gewichteter Mittelwert aller Messpunkt-Koordinaten
        lat_router = np.average(gruppe["lat"], weights=gruppe["gewicht"])
        lon_router = np.average(gruppe["lon"], weights=gruppe["gewicht"])

        # Bestimme häufigste SSID für diesen Router (kann variabel sein)
        ssid_router = gruppe["ssid"].mode().iloc[0] if gruppe["ssid"].notna().any() else "Unbekannt"

        # Sammle Router-Informationen
        router_liste.append({
            "mac": mac,  # MAC-Adresse des Routers
            "ssid": ssid_router,  # SSID (Netzwerkname)
            "router_lat": lat_router,  # Geschätzte Breitengrad
            "router_lon": lon_router,  # Geschätzte Längengrad
            "messpunkte": len(gruppe),  # Anzahl der Messpunkte für diese Triangulation
            "mittleres_rssi": gruppe["rssi"].mean()  # Durchschnittliches RSSI-Signal
        })

    # Konvertiere Liste der Router in DataFrame
    df_router_pos = pd.DataFrame(router_liste)
    return df_router_pos