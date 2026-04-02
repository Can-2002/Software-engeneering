from dataloader.loader import einlesen_daten

def daten_laden():
    genutzte_csv = "/workspaces/Software-engeneering/data/Testdaten2.csv"
    df = einlese_daten(genutzte_csv)
    print(df.head())

if __name__ == "__main__":
    daten_laden()
