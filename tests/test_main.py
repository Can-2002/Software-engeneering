# Datei: test_main.py
# Zweck: Python Modul

# Dieses Modul enthält Tests für die Hauptfunktionen.

# Imports für dieses Modul
import sys  # Import für Systemfunktionen
import os   # Import für Betriebssystemfunktionen

# Pfad zum src-Verzeichnis hinzufügen, um Module zu importieren
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

# Import der Funktionen, die getestet werden sollen
from main import main


# Test für die main-Funktion
def test_main_exists():
    """Überprüft, dass die main-Funktion existiert und aufgerufen werden kann."""
    # Diese Test überprüft nur, dass die Funktion definiert ist
    # Ein vollständiger Test würde die Funktionalität überprüfen
    assert callable(main), "main() sollte eine aufrufbare Funktion sein"
