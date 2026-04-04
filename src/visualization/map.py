# Datei: map.py

import folium
import pandas as pd
import webbrowser


# -----------------------------------------
# NEU: RSSI → Distanz
# -----------------------------------------
def rssi_zu_distanz(rssi, tx_power=-45, n=3.0):
    return 10 ** ((tx_power - rssi) / (10 * n))


# Funktion map_erstellen
def map_erstellen(df_datengefiltert, df_router_pos):

    weg_punkte = df_datengefiltert[["lat", "lon"]].values.tolist()

    m = folium.Map(
        location=[df_datengefiltert["lat"].mean(), df_datengefiltert["lon"].mean()],
        zoom_start=19,
        tiles="CartoDB positron"
    )

    # -----------------------------------------
    # START / ENDE
    # -----------------------------------------
    folium.Marker(weg_punkte[0], popup="Start", icon=folium.Icon(color="green")).add_to(m)
    folium.Marker(weg_punkte[-1], popup="Ende", icon=folium.Icon(color="red")).add_to(m)

    # -----------------------------------------
    # WEG
    # -----------------------------------------
    gelaufener_weg = folium.FeatureGroup(name="Pfad/Linie", show=True)
    folium.PolyLine(weg_punkte, color="blue", weight=4, opacity=0.7).add_to(gelaufener_weg)
    gelaufener_weg.add_to(m)

    # -----------------------------------------
    # ALLE MESSPUNKTE (global)
    # -----------------------------------------
    messpunkte = folium.FeatureGroup(name="Messpunkte (alle)", show=True)

    for _, row in df_datengefiltert.iterrows():
        folium.CircleMarker(
            location=[row["lat"], row["lon"]],
            radius=3,
            color="red",
            fill=True,
            popup=f'RSSI {row["rssi"]} | MAC {row["mac"]}'
        ).add_to(messpunkte)

    messpunkte.add_to(m)

    # -----------------------------------------
    # ALLE ROUTER (ein Layer)
    # -----------------------------------------
    alle_router = folium.FeatureGroup(name="Alle Router", show=True)

    for _, row in df_router_pos.iterrows():
        folium.Marker(
            location=[row["router_lat"], row["router_lon"]],
            popup=f'SSID: {row["ssid"]}<br>MAC: {row["mac"]}',
            tooltip=f'{row["ssid"]} | {row["mac"]}'
        ).add_to(alle_router)

    alle_router.add_to(m)

    # -----------------------------------------
    # NEU: EINZELNE ROUTER (pro MAC)
    # -----------------------------------------
    for _, router_row in df_router_pos.iterrows():

        mac = router_row["mac"]
        ssid = router_row["ssid"] if pd.notna(router_row["ssid"]) else "Unbekannt"

        # alle Messpunkte dieser MAC
        df_mac = df_datengefiltert[df_datengefiltert["mac"] == mac]

        if df_mac.empty:
            continue

        layer_name = f"{ssid} | {mac}"
        router_layer = folium.FeatureGroup(name=layer_name, show=False)

        # -----------------------------
        # Router Marker
        # -----------------------------
        folium.Marker(
            location=[router_row["router_lat"], router_row["router_lon"]],
            popup=f"<b>Router</b><br>SSID: {ssid}<br>MAC: {mac}",
            icon=folium.Icon(color="blue", icon="wifi", prefix="fa")
        ).add_to(router_layer)

        # -----------------------------
        # Messpunkte + Kreise
        # -----------------------------
        for _, messung in df_mac.iterrows():

            rssi = messung["rssi"]
            radius = rssi_zu_distanz(rssi)

            # Messpunkt
            folium.CircleMarker(
                location=[messung["lat"], messung["lon"]],
                radius=4,
                color="red",
                fill=True,
                popup=f"RSSI: {rssi}"
            ).add_to(router_layer)

            # Kreis (Distanz)
            folium.Circle(
                location=[messung["lat"], messung["lon"]],
                radius=radius,
                color="blue",
                fill=False,
                weight=1,
                opacity=0.4
            ).add_to(router_layer)

        router_layer.add_to(m)

    # -----------------------------------------
    # LAYER CONTROL
    # -----------------------------------------
    folium.LayerControl(collapsed=False).add_to(m)


    # -----------------------------------------
    # SPEICHERN + ÖFFNEN
    # -----------------------------------------
    m.save("mein_gelaufener_weg.html")
    webbrowser.open("http://localhost:8000/mein_gelaufener_weg.html")
