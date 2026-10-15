import pytest
from termdown.utils import normalize_text

# Decision Coverage (normalize_text)
# Decision A: if unicodedata.category(c) != "Mn"
# True: character is retained
# False: combining diacritical mark is removed

def test_normalize_german_lowercase():
    assert normalize_text("äöüß") == "aeoeuess"
    # German lowercase characters are replaced with their equivalents

def test_normalize_german_uppercase():
    assert normalize_text("ÄÖÜ") == "AeOeUe"
    # German uppercase characters are replaced with their equivalents

def test_decision_a_true():
    assert normalize_text("hello123!") == "hello123!"
    # A is True -> ordinary characters are retained

def test_decision_a_false():
    assert normalize_text("e\u0301") == "e"
    # A is False -> combining acute accent (category Mn) is removed

def test_normalize_accented_character():
    assert normalize_text("café") == "cafe"
    # NFD decomposes é into e + combining accent, which is removed

def test_normalize_empty_string():
    assert normalize_text("") == ""
    # Empty input produces empty output