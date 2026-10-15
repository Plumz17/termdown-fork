import pytest
from termdown.utils import normalize_text

# Decision Coverage (normalize_text)
# Decision A: if unicodedata.category(c) != "Mn"
# True: character is retained
# False: combining diacritical mark is removed
def test_decision_a_true():
    assert normalize_text("hello123!") == "hello123!"
    # A is True -> ordinary characters are retained

def test_decision_a_false():
    assert normalize_text("e\u0301") == "e"
    # A is False -> combining acute accent (category Mn) is removed

# Equivalence Partitioning (normalize_text)
@pytest.mark.parametrize(
    "text, expected",
    [
        ("hello123!", "hello123!"),  # ordinary characters
        ("äöüß", "aeoeuess"),        # German lowercase characters
        ("ÄÖÜ", "AeOeUe"),           # German uppercase characters
        ("café", "cafe"),            # accented characters
    ],
)
def test_ep_valid_groups(text, expected):
    assert normalize_text(text) == expected

# Edge Case Testing (normalize_text)
def test_edge_empty_string():
    assert normalize_text("") == ""
    # Empty input should produce empty output
