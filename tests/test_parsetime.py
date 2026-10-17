import pytest
from datetime import datetime, timezone, timedelta
from dateutil import tz
from dateutil.parser import parse

from termdown.utils import parse_timestr, parse_timedelta

time_components = ["1y","1d","1h","1m","1s"]

seconds = {}
for time in time_components:
    seconds[time] = parse_timedelta(time)
    
# print(seconds)
# print(parse_timedelta(""))
print(parse_timestr("99-10-10"))

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

# Decision Coverage (parse_timestr, ignore microseconds)
# A: ordered duration time input
def test_decision_str_a():
    parsed_time = parse_timestr("1y 1d 1h 1m 1s").replace(microsecond=0)
    expected = (datetime_now + timedelta(seconds=(31557600 + 86400 + 3600 + 60 + 1))).replace(microsecond=0)
    assert parsed_time == expected
    
# B: integer in string input for duration in seconds
def test_decision_str_b():
    parsed_time = parse_timestr("3000").replace(microsecond=0)
    expected = (datetime_now + timedelta(seconds=3000)).replace(microsecond=0)
    assert parsed_time == expected
    
# C: datetime input
# Invalid datetime, raise ValueError
def test_decision_str_c_invalid_datetime():
    with pytest.raises(ValueError):
        parse_timestr("2027-13-32 24:60:60")
        
# No timezone, use local timezone
def test_decision_str_c_no_timezone():
    date_time = "2026-12-31 10:10:10"
    parsed_time = parse_timestr(date_time).replace(microsecond=0)
    expected = parse(date_time).replace(tzinfo=tz.tzlocal()).astimezone(timezone.utc).replace(microsecond=0)
    assert parsed_time == expected
   
# Input only time, use tomorrow date
def test_decision_str_c_before_now():
    date_time = "2026-09-16 10:10:10"
    parsed_time = parse_timestr(date_time).replace(microsecond=0)
    expected = (parse(date_time) + timedelta(days=1)).replace(microsecond=0)
    assert parsed_time == expected

# Boundary Value Analysis (parse_timedelta) 
@pytest.mark.parametrize(
    "values, expected",
    [
        ("-1y", 0), ("0y", 0), ("1y", 31557600), # year
        ("-1d", 0), ("0d", 0), ("1d", 86400), # day
        ("-1h", 0), ("0h", 0), ("1h", 3600), # hour
        ("-1m", 0), ("0m", 0), ("1m", 60), # minute
        ("-1s", 0), ("0s", 0), ("1s", 1), # second
    ]
)
def test_bva_boundaries(values, expected):
    assert parse_timedelta(values) == expected

# Boundary Value Analysis (parse_timestr) 
@pytest.mark.parametrize(
    "datetimes, expected",
    [
        # year
        
        # day
        # hour
        # minute
        # second
    ]
)
def test_bva_boudaries_str_valid(datetimes, expected):
    assert parse_timestr(datetimes) == expected

# Error Guessing (parse_timedelta)


# Error Guessing (parse_timestr)
