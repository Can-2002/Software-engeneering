import pandas as ps
def filter_data(df_datenBereinigt):
    counts = df_datenBereinigt["mac"].value_counts()
    df_gefiltert = df_datenBereinigt[df_datenBereinigt["mac"].isin(counts[counts >= 3].index)]
    return df_gefiltert

