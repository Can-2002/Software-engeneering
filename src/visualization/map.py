import folium
import pandas as pd
import webbrowser


def map_erstellen(df_datengefiltert,df_router_pos ):
    """Erzeugt eine interaktive Karte aus gefilterten GPS-Daten."""

    # Punkte extrahieren (Latitude, Longitude)
    weg_punkte = df_datengefiltert[["lat", "lon"]].values.tolist()

    # Basis-Karte zentrieren auf Durchschnitt der Koordinaten
    m = folium.Map(
        location=[df_datengefiltert["lat"].mean(), df_datengefiltert["lon"].mean()],
        zoom_start=19,
        tiles="CartoDB positron"
    )

    # Start- und Endmarker einfügen
    folium.Marker(weg_punkte[0], popup="Start", icon=folium.Icon(color="green")).add_to(m)
    folium.Marker(weg_punkte[-1], popup="Ende", icon=folium.Icon(color="red")).add_to(m)

    # Linienverbindung aller Wegepunkte darstellen
    gelaufener_weg = folium.FeatureGroup(name="Pfad/Linie", show=True)
    folium.PolyLine(weg_punkte, color="blue", weight=4, opacity=0.7).add_to(gelaufener_weg)
    gelaufener_weg.add_to(m)

    messpunkte = folium.FeatureGroup(name="Messpunkte", show=True)
    for index, row in df_datengefiltert.iterrows():
        folium.CircleMarker(
                location=[row["lat"], row["lon"]],
                radius=4,
                color="red",
                fill=True,
                popup=f'RSSI {row["rssi"]}'
        ).add_to(messpunkte)
    messpunkte.add_to(m)

    routerpositionen = folium.FeatureGroup(name="Router (geschätzt)", show=True)
    for index, row in df_router_pos.iterrows():
        folium.CircleMarker(
            location=[row["lat"], row["lon"]],
            radius=4,
                color="blue",
                fill=True,
                popup=f'mac {row["mac"]}'
        ).add_to(routerpositionen)
    routerpositionen.add_to(m)
        


    folium.LayerControl(collapsed=False).add_to(m)
    
    custom_css = """
    <style>
        /* Das Icon zum Ausklappen vergrößern */
        .leaflet-control-layers-toggle {
            width: 60px !important;
            height: 60px !important;
            background-size: 40px 40px !important;
        }
        /* Das ausgeklappte Menü anpassen */
        .leaflet-control-layers-expanded {
            font-size: 20px !important; /* Schriftgröße */
            padding: 15px !important;   /* Innenabstand */
            min-width: 200px !important; /* Mindestbreite */
        }
        /* Die Checkboxen selbst vergrößern */
        .leaflet-control-layers-selector {
            transform: scale(1.5);      /* Macht die Checkbox 1.5x größer */
            margin-right: 10px !important;
        }
    </style>
    """

    # 4. Das CSS in das HTML-Dokument der Karte einfügen
    m.get_root().header.add_child(folium.Element(custom_css))




    m.save("mein_gelaufener_weg.html")
    webbrowser.open("http://localhost:8000/mein_gelaufener_weg.html")
