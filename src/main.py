from dataloader.loader import einlese_daten
from processing.cleaning import datenbereinigung
def main():
    genutzte_csv = "/workspaces/Software-engeneering/data/Testdaten1.csv"
    df_rohdaten = einlese_daten(genutzte_csv)
    df_datenBereinigt = datenbereinigung(df_rohdaten)

    print(df_datenBereinigt.head())


if __name__ == "__main__":
    main()









