# Dieses Modul enthält Tests für die Hauptfunktionen.

import sys  # Import für Systemfunktionen
import os   # Import für Betriebssystemfunktionen

# Pfad zum src-Verzeichnis hinzufügen, um Module zu importieren
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.main import hello  # Import der zu testenden Funktion (Hinweis: Diese Funktion existiert möglicherweise nicht in main.py)

def test_hello():
    # Testet die hello-Funktion
    assert hello() == "Hello World"  # Überprüft, ob die Funktion "Hello World" zurückgibt