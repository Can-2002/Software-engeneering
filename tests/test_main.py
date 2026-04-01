import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.main import hello

def test_hello():
    assert hello() == "Hello World"