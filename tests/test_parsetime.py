import pytest
from datetime import datetime, timezone, timedelta
from termdown.utils import parse_timestr, parse_timedelta

time_components = ["1y","1d","1h","1m","1s"]

seconds = {}
for time in time_components:
    seconds[time] = parse_timedelta(time)
    
print(seconds)
print(parse_timestr("2026-10-15"))

datetime_now = datetime.now(timezone.utc)
print(datetime_now)

# Decision Coverage (parse_timedelta)
# A: Time duration input matches the regex, return None if no matches
def test_decision_a_false():
    # Empty string input
    assert parse_timedelta("") == None
    
    # All component units are invalid
    assert parse_timedelta("1a 2b 3c 4d 5e") == None
    
    # All component reverse-ordered
    assert parse_timedelta("1s 1m 1h 1d 1y") == None
    
def test_decision_a_true():
    # At least one component valid
    assert parse_timedelta("1s") == 1
    
    # Has year or day component
    assert parse_timedelta("1y 1d 1h") == 31557600 + 86400 + 3600

# Decision Coverage (parse_timestr)
# A: ordered duration time input
def test_decision_delta_a():
    assert parse_timestr("1y 1d 1h 1m 1s") == datetime_now + timedelta(seconds=(31557600 + 86400 + 3600 + 60 + 1))
    
# B: integer in string input for duration in seconds
def test_decision_delta_b():
    assert parse_timestr("3000") == datetime_now + timedelta(seconds=3000)
    
# C: date

# Boundary Value Analysis (parse_timedelta) 

# Boundary Value Analysis (parse_timestr) 

# Error Guessing (parse_timedelta)

# Error Guessing (parse_timestr)