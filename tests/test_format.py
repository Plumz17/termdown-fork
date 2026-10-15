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


# Equivalance Partitioning (format_seconds)
@pytest.mark.parametrize(
    "seconds, expected",
    [
        (-5, "-5"), #negative group
        (30, "30"), #seconds group (below a minute)
        (300, "5m"), #minutes group
        (7200, "2h"), #hours group
        (259200, "3d"), #days group
        (63201600, "2y 1d"), #years group
        (10**9, "31y 251d 7h 46m 40s"), # years group, but with very large value
        (0.2, "1"), #decimal group: should round up
    ],
)
def test_ep_valid_groups(seconds, expected):
    assert format_seconds(seconds) == expected
 
def test_ep_invalid_group_text():
    with pytest.raises(TypeError):
        format_seconds("abc")

# Equivalance Partitioning (format_seconds_alt)
@pytest.mark.parametrize(
    "seconds, expected",
    [
        # Under a day (Supposed to be 3 blocks)
        (30, "00:00:30"), # seconds group
        (300, "00:05:00"), # minutes group
        (7200, "02:00:00"), # hours group

        (259200, "03:00:00:00"), # days group (supposed to be 4 blocks)
        (63201600, "02:01:00:00:00"), # 1 year+: (supposed to be 5 bkocks)
        (10**9, "31:251:07:46:40"), # very large, 3-digit day block
        (0.2, "00:00:01"), #decimal group: should round up
    ],
)
def test_ep_alt_valid_groups(seconds, expected):
    assert format_seconds_alt(seconds) == expected
 
def test_ep_alt_invalid_group_text():
    with pytest.raises(TypeError):
        format_seconds_alt("abc")

# Boundary Value Analysis (format_seconds)
@pytest.mark.parametrize(
    "seconds, expected",
    [
        (-1, "-1"), (0, "0"), (1, "1"), # around 0
        (59, "59"), (60, "60"), (61, "1m 1s"), # around 60
        (119, "1m 59s"), (120, "2m"), (121, "2m 1s"), # around 120
        (3599, "59m 59s"), (3600, "1h"), (3601, "1h 1s"), # around 3600
        (86399, "23h 59m 59s"), (86400, "1d"), (86401, "1d 1s"), # araound 86400
        (31557599, "365d 5h 59m 59s"), (31557600, "1y"), (31557601, "1y 1s"), # around 31557600
        (60.0, "60"), (60.01, "1m 1s"), # test decimals
    ],
)
def test_bva_boundaries(seconds, expected):
    assert format_seconds(seconds) == expected
 
# hide_seconds has its own boundary: total_seconds > 60
@pytest.mark.parametrize(
    "seconds, expected",
    [(59, "59"), (60, "60"), (61, "1m"), (3601, "1h")],
)

def test_bva_hide_seconds_boundary(seconds, expected):
    assert format_seconds(seconds, hide_seconds=True) == expected