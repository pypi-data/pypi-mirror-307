import pytest
from recipy.utils import parse_time


@pytest.mark.parametrize("duration,expected_minutes", [
    ("PT2H30M", 150),  # 2 hours and 30 minutes
    ("PT2H", 120),     # 2 hours only
    ("PT45M", 45),     # 45 minutes only
    ("PT0H0M", 0),     # 0 hours and 0 minutes
    ("PT1H", 60),      # 1 hour only
])
def test_valid_iso_duration(duration, expected_minutes):
    assert parse_time(duration) == expected_minutes


@pytest.mark.parametrize("invalid_duration", [
    "2H30M",      # Missing 'PT' prefix
    "PT2H30",     # Missing 'M' after minutes
    "PT2M30H",    # Incorrect order
    "P2H30M",     # Incorrect prefix
    "PT",         # Incomplete duration
])
def test_invalid_iso_duration(invalid_duration):
    assert parse_time(invalid_duration) is None


@pytest.mark.parametrize("empty_input", [
    "",           # Empty string
    "   ",        # Whitespace string
    "PT",         # 'PT' with no time
])
def test_empty_or_no_time(empty_input):
    assert parse_time(empty_input) is None


@pytest.mark.parametrize("duration,expected_minutes", [
    ("PT30M", 30),    # 30 minutes only
    ("PT1H30M", 90),  # 1 hour and 30 minutes
    ("PT1M", 1),      # 1 minute only
])
def test_minutes_only(duration, expected_minutes):
    assert parse_time(duration) == expected_minutes


@pytest.mark.parametrize("duration,expected_minutes", [
    ("PT2H", 120),    # 2 hours only
    ("PT5H", 300),    # 5 hours only
])
def test_hours_only(duration, expected_minutes):
    assert parse_time(duration) == expected_minutes
