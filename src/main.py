import seaborn as sns
import matplotlib.pyplot as plt

def seaborn_test():
    # Beispiel-Daten (kommt von seaborn selbst)
    data = sns.load_dataset("iris")

    # Plot erstellen
    sns.scatterplot(data=data, x="sepal_length", y="sepal_width")

    # Titel
    plt.title("Seaborn Iris Plot")

    # Bild speichern
    plt.savefig("seaborn_plot.png")
    plt.close()

    # Terminal-Ausgabe
    print("✅ Seaborn Plot erstellt!")
    print("📁 Datei: seaborn_plot.png")
    print("📊 Datensatz:", data.shape)

if __name__ == "__main__":
    seaborn_test()