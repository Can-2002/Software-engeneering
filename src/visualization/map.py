# Datei: map.py
# Zweck: Visualisierung der Daten auf einer interaktiven Karte

# Imports für dieses Modul
import folium  # Kartenbibliothek für interaktive Karten
import pandas as pd  # pandas wird für DataFrame-Verarbeitung verwendet
import webbrowser  # Öffnet die HTML-Datei im Standard-Browser


def rssi_zu_distanz(rssi, tx_power=-45, n=3.0):
    """Wandelt RSSI-Wert in eine ungefähre Distanz um.
    
    Parameter:
    - rssi: Der RSSI-Wert (Received Signal Strength Indicator)
    - tx_power: Geschätzter RSSI-Wert bei 1 Meter Entfernung (Standard: -45 dBm)
    - n: Path-Loss-Exponent für die Distanzberechnung (Standard: 3.0)
    
    Rückgabewert:
    - Distanz in Metern (geschätzt)
    """
    return 10 ** ((tx_power - rssi) / (10 * n))


def map_erstellen(df_datengefiltert, df_router_pos, df_route_geschaetzt):
    """Erzeugt eine interaktive Karte aus gefilterten GPS-Daten.
    
    Parameter:
    - df_datengefiltert: DataFrame mit gefilterten Messdaten (lat, lon, ssid, mac, rssi)
    - df_router_pos: DataFrame mit geschätzten Routerpositionen
    - df_route_geschaetzt: DataFrame mit der geschätzten Route aus WLAN-Daten
    
    Rückgabewert:
    - Speichert die Karte als HTML-Datei ('mein_gelaufener_weg.html')
    """

    # Extrahiere alle Wichtungspunkte (GPS-Koordinaten) aus den Messdaten
    weg_punkte = df_datengefiltert[["lat", "lon"]].values.tolist()

    # Erstelle eine neue Karte mit dem Mittelpunkt basierend auf den Messdaten
    m = folium.Map(
        location=[df_datengefiltert["lat"].mean(), df_datengefiltert["lon"].mean()],
        zoom_start=19,
        tiles="CartoDB positron"  # Verwende CartoDB Positron als Kartenhintergrund
    )

    # ========== Start- und Endpunkt markieren ==========
    # Start / Ende
    folium.Marker(
        weg_punkte[0],
        popup="Start",
        icon=folium.Icon(color="green")
    ).add_to(m)

    folium.Marker(
        weg_punkte[-1],
        popup="Ende",
        icon=folium.Icon(color="red")  # Roter Marker für Endpunkt
    ).add_to(m)

    # ========== Gelaufener Weg visualisieren ==========
    # Gelaufener Weg
    gelaufener_weg = folium.FeatureGroup(name="Pfad/Linie", show=True)
    folium.PolyLine(
        weg_punkte,
        color="blue",
        weight=4,
        opacity=0.7
    ).add_to(gelaufener_weg)  # Linie zur Feature-Group hinzufügen
    gelaufener_weg.add_to(m)  # Feature-Group zur Karte hinzufügen

    # ========== Alle Messpunkte als rote Punkte anzeigen ==========
    messpunkte = folium.FeatureGroup(name="Messpunkte (alle)", show=False)
    for _, row in df_datengefiltert.iterrows():
        folium.CircleMarker(
            location=[row["lat"], row["lon"]],
            radius=3,
            color="red",
            fill=True,
            fill_opacity=0.8,
            popup=f'SSID: {row["ssid"]}<br>MAC: {row["mac"]}<br>RSSI: {row["rssi"]}'
        ).add_to(messpunkte)
    messpunkte.add_to(m)  # Feature-Group mit Messpunkten zur Karte hinzufügen

    # ========== Alle erkannten Router anzeigen ==========
    alle_router = folium.FeatureGroup(name="Alle Router", show=True)
    for _, row in df_router_pos.iterrows():
        folium.Marker(
            location=[row["router_lat"], row["router_lon"]],
            popup=f'SSID: {row["ssid"]}<br>MAC: {row["mac"]}',
            tooltip=f'{row["ssid"]} | {row["mac"]}'
        ).add_to(alle_router)
    alle_router.add_to(m)  # Feature-Group mit allen Routern zur Karte hinzufügen

    # ========== Definiere Farbpalette für Router-Visualisierung ==========
    farben = [
        "red",
        "blue",
        "green",
        "purple",
        "orange",
        "darkred",
        "lightred",
        "beige",
        "darkblue",
        "darkgreen",
        "cadetblue",
        "darkpurple",
        "pink",
        "lightblue",
        "lightgreen",
        "gray",
        "black"
    ]  # 17 verschiedene Farben für bis zu 17 Router

    # ========== Visualisiere jeden Router separat mit Messpunkten und Signalradius ==========
    for i, (_, router_row) in enumerate(df_router_pos.iterrows()):
        mac = router_row["mac"]
        ssid = router_row["ssid"] if pd.notna(router_row["ssid"]) else "Unbekannt"

        # Wähle Farbe basierend auf Router-Index (zyklisch durch Farbpalette)
        farbe = farben[i % len(farben)]

        # Filtere nur Messungen für diese spezifische MAC-Adresse
        df_mac = df_datengefiltert[df_datengefiltert["mac"] == mac].copy()

        # Überspringe Router ohne Messdaten
        if df_mac.empty:
            continue

        # Erstelle Feature-Group für diesen Router (Name wird in der Legende angezeigt)
        layer_name = f"{ssid} | {mac}"
        router_layer = folium.FeatureGroup(name=layer_name, show=False)

        # Routerposition
        folium.Marker(
            location=[router_row["router_lat"], router_row["router_lon"]],
            popup=(
                f"<b>Geschätzter Router</b><br>"
                f"SSID: {ssid}<br>"
                f"MAC: {mac}<br>"
                f"Messpunkte: {router_row['messpunkte']}<br>"
                f"Mittleres RSSI: {router_row['mittleres_rssi']:.2f}"
            ),
            tooltip=f"Router: {ssid} | {mac}",
            icon=folium.Icon(color=farbe)  # Marker mit der Router-Farbe
        ).add_to(router_layer)

        # Iteriere über alle Messpunkte für diesen Router
        for _, messung in df_mac.iterrows():
            # Extrahiere RSSI und berechne geschätzte Signalstärke-Radius
            rssi = messung["rssi"]
            radius = rssi_zu_distanz(rssi)  # Umrechnung RSSI -> Distanz in Metern

            # Bereite Info-Text für Popup vor
            popup_text = (
                f"<b>Messpunkt</b><br>"
                f"SSID: {ssid}<br>"
                f"MAC: {mac}<br>"
                f"RSSI: {rssi}<br>"
                f"Radius: {radius:.2f} m"  # Geschätzte Reichweite
            )

            # Marker für Messpunkt (kleine Punkte auf der Karte)
            folium.CircleMarker(
                location=[messung["lat"], messung["lon"]],
                radius=4,
                color=farbe,
                fill=True,
                fill_color=farbe,
                fill_opacity=0.9,
                popup=popup_text,
                tooltip=f"{ssid} | RSSI {rssi}"  # Tooltip beim Hover
            ).add_to(router_layer)  # Messpunkt zur Layer hinzufügen

            # Signalstärke-Kreis basierend auf berechneter Distanz
            folium.Circle(
                location=[messung["lat"], messung["lon"]],
                radius=radius,
                color=farbe,
                fill=False,  # Kreis ohne Füllung (nur der Umriss ist sichtbar)
                weight=2,  # Dicke der Linie
                opacity=0.45,  # Transparenz
                popup=popup_text
            ).add_to(router_layer)  # Signalkreis zur Layer hinzufügen

        # Füge die Router-spezifische Layer zur Karte hinzu
        router_layer.add_to(m)

        # ========== Geschätzte Route aus WLAN-Triangulation visualisieren =========
    geschaetzte_route = folium.FeatureGroup(
        name="Geschätzte Route (WLAN)",
        show=True  # Route ist standardmäßig sichtbar
    )

    # Überprüfe, ob Routendaten vorhanden sind
    if df_route_geschaetzt is not None and not df_route_geschaetzt.empty:
        # Extrahiere Route-Koordinaten als Liste
        route_punkte = df_route_geschaetzt[["lat", "lon"]].values.tolist()

    # Verbindungslinie für geschätzte Route zeichnen
        if len(route_punkte) > 1:
            folium.PolyLine(
                route_punkte,
                color="purple",
                weight=4,
                opacity=0.8,
                tooltip="Geschätzte Route"
            ).add_to(geschaetzte_route)

    # Einzelne Messpunkte der geschätzten Route als Marker
        for _, row in df_route_geschaetzt.iterrows():
            folium.CircleMarker(
                location=[row["lat"], row["lon"]],
                radius=4,
                color="purple",
                fill=True,
                fill_opacity=0.8,
                popup=f'Router genutzt: {row["anzahl_router"]}'
            ).add_to(geschaetzte_route)

    geschaetzte_route.add_to(m)  # Route-Layer zur Karte hinzufügen

    # ========== Layer-Kontrolle hinzufügen ==========
    # Erlaubt dem Benutzer, Layer ein- und auszuschalten
    folium.LayerControl(collapsed=False).add_to(m)

    # ========== Karte als HTML speichern und öffnen ==========
    # Speichere die Karte als HTML-Datei
    m.save("mein_gelaufener_weg.html")
    # Öffne die HTML-Datei im Standard-Webbrowser über lokalen Server
    webbrowser.open("http://localhost:8000/mein_gelaufener_weg.html")