import pytest
from termdown.utils import format_seconds, format_seconds_alt

# Decision Coverage (format_seconds)
# Decision A: if seconds <= 60
# Decision B: if seconds >= period_seconds and not (hide_seconds and period == "s")
def test_decision_a_true():
    assert format_seconds(60) == "60" # A is True -> early return
 
def test_decision_a_false():
    assert format_seconds(61) == "1m 1s" # A is False -> loop runs
 
def test_decision_b_true():
    assert format_seconds(125) == "2m 5s" # a unit is used (125 -> 2 minutes, 5 seconds)
 
def test_decision_b_false():
    assert format_seconds(3600) == "1h" # 3600 -> "1h": the minutes and seconds units are skipped

# Decision Coverage (format_seconds_alt)
# Decision A: if hide_seconds and period_seconds == 1 and total_seconds > 60
# Decision B: if actual_period_value > 0
# Decision C: elif 86400 > period_seconds or total_seconds > period_seconds
def test_decision_alt_a_true():
    assert format_seconds_alt(61, hide_seconds=True) == "00:01"
 
def test_decision_alt_a_false():
    assert format_seconds_alt(61, hide_seconds=False) == "00:01:01"

def test_decision_alt_b_true_and_false():
    # 3661: the year/day blocks have value 0 (B False), hour/min/sec > 0 (B True)
    assert format_seconds_alt(3661) == "01:01:01"
 
def test_decision_alt_c_true():
    # 45: a zero hour block is still printed as "00:" (C True)
    assert format_seconds_alt(45) == "00:00:45"
 
def test_decision_alt_c_false():
    # 3661: the zero year and day blocks are NOT printed (C False)
    assert format_seconds_alt(3661).count(":") == 2