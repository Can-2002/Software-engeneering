import folium 
import pandas as pd
def map_erstellen(df_datengefiltert):
    weg_punkte = df_datengefiltert[['lat', 'lon']].values.tolist()

    m = folium.Map(location= [df_datengefiltert["lat"].mean(), df_datengefiltert["lon"].mean()], zoom_start=13, tiles="CartoDB positron")
    folium.PolyLine(weg_punkte, color ="blue", weight = 4, opacity =0.7).add_to(m)
    folium.Marker(weg_punkte[0], popup="Start", icon=folium.Icon(color="green")).add_to(m)
    m.save("mein_gelaufener_weg.html")