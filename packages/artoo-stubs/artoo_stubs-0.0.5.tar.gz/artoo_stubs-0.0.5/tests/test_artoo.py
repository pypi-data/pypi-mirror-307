from src.artoo import hello


def test_artoo():
    result = hello()
    assert result == "Hi, I'm Artoo"
