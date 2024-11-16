import pytest
from main import run

def test_messages():
    response = run()
    print("AI Response:", response)