import folium
import pandas as pd
import webbrowser


def rssi_zu_distanz(rssi, tx_power=-45, n=3.0):
    return 10 ** ((tx_power - rssi) / (10 * n))


def map_erstellen(df_datengefiltert, df_router_pos, df_route_geschaetzt):
    """Erzeugt eine interaktive Karte aus gefilterten GPS-Daten."""

    weg_punkte = df_datengefiltert[["lat", "lon"]].values.tolist()

    m = folium.Map(
        location=[df_datengefiltert["lat"].mean(), df_datengefiltert["lon"].mean()],
        zoom_start=19,
        tiles="CartoDB positron"
    )

    # Start / Ende
    folium.Marker(
        weg_punkte[0],
        popup="Start",
        icon=folium.Icon(color="green")
    ).add_to(m)

    folium.Marker(
        weg_punkte[-1],
        popup="Ende",
        icon=folium.Icon(color="red")
    ).add_to(m)

    # Gelaufener Weg
    gelaufener_weg = folium.FeatureGroup(name="Pfad/Linie", show=True)
    folium.PolyLine(
        weg_punkte,
        color="blue",
        weight=4,
        opacity=0.7
    ).add_to(gelaufener_weg)
    gelaufener_weg.add_to(m)

    # Alle Messpunkte
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
    messpunkte.add_to(m)

    # Alle Router
    alle_router = folium.FeatureGroup(name="Alle Router", show=True)
    for _, row in df_router_pos.iterrows():
        folium.Marker(
            location=[row["router_lat"], row["router_lon"]],
            popup=f'SSID: {row["ssid"]}<br>MAC: {row["mac"]}',
            tooltip=f'{row["ssid"]} | {row["mac"]}'
        ).add_to(alle_router)
    alle_router.add_to(m)

    # Farbpalette für einzelne Router
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
    ]

    # Einzelne Router pro MAC
    for i, (_, router_row) in enumerate(df_router_pos.iterrows()):
        mac = router_row["mac"]
        ssid = router_row["ssid"] if pd.notna(router_row["ssid"]) else "Unbekannt"

        # Farbe für diesen Router
        farbe = farben[i % len(farben)]

        # Nur Messungen dieser MAC
        df_mac = df_datengefiltert[df_datengefiltert["mac"] == mac].copy()

        if df_mac.empty:
            continue

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
            icon=folium.Icon(color=farbe)
        ).add_to(router_layer)

        # Messpunkte und Kreise nur für diesen Router
        for _, messung in df_mac.iterrows():
            rssi = messung["rssi"]
            radius = rssi_zu_distanz(rssi)

            popup_text = (
                f"<b>Messpunkt</b><br>"
                f"SSID: {ssid}<br>"
                f"MAC: {mac}<br>"
                f"RSSI: {rssi}<br>"
                f"Radius: {radius:.2f} m"
            )

            # Messpunkt
            folium.CircleMarker(
                location=[messung["lat"], messung["lon"]],
                radius=4,
                color=farbe,
                fill=True,
                fill_color=farbe,
                fill_opacity=0.9,
                popup=popup_text,
                tooltip=f"{ssid} | RSSI {rssi}"
            ).add_to(router_layer)

            # Kreis
            folium.Circle(
                location=[messung["lat"], messung["lon"]],
                radius=radius,
                color=farbe,
                fill=False,
                weight=2,
                opacity=0.45,
                popup=popup_text
            ).add_to(router_layer)

        router_layer.add_to(m)

        # -----------------------------------------
# NEU: Geschätzte Route aus WLAN
# -----------------------------------------
    geschaetzte_route = folium.FeatureGroup(
        name="Geschätzte Route (WLAN)",
        show=True
)

    if df_route_geschaetzt is not None and not df_route_geschaetzt.empty:

        route_punkte = df_route_geschaetzt[["lat", "lon"]].values.tolist()

    # Linie
        if len(route_punkte) > 1:
            folium.PolyLine(
                route_punkte,
                color="purple",
                weight=4,
                opacity=0.8,
                tooltip="Geschätzte Route"
            ).add_to(geschaetzte_route)

    # Punkte
        for _, row in df_route_geschaetzt.iterrows():
            folium.CircleMarker(
                location=[row["lat"], row["lon"]],
                radius=4,
                color="purple",
                fill=True,
                fill_opacity=0.8,
                popup=f'Router genutzt: {row["anzahl_router"]}'
            ).add_to(geschaetzte_route)

    geschaetzte_route.add_to(m)

    folium.LayerControl(collapsed=False).add_to(m)


    m.save("mein_gelaufener_weg.html")
    webbrowser.open("http://localhost:8000/mein_gelaufener_weg.html")