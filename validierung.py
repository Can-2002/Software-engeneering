import pandas as pd

def datenpruefung (df_rohdaten, name = "Dataframe"):
    if df_rohdaten is None:
        raise ValueError (f"{name} ist None")
    
    if df_rohdaten.empty:
        raise  ValueError (f"{name}ist Leer")
    
    
