# Dieses Modul enthält Tests für die Hauptfunktionen.

import sys  # Import für Systemfunktionen
import os   # Import für Betriebssystemfunktionen

# Pfad zum src-Verzeichnis hinzufügen, um Module zu importieren
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

# Testet die vorhandene hello-Funktion in src/main.py
from main import hello


def test_hello():
    # Überprüft, ob hello() den erwarteten Text liefert
    assert hello() == "Hello World"
