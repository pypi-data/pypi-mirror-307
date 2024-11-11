import pytest
from recipy.utils import normalize_temperatures


@pytest.mark.parametrize("input_text,expected", [
    ("350 degrees F", "350°F"),
    ("212 degrees F", "212°F"),
    ("100 degrees F", "100°F"),
])
def test_fahrenheit_normalization(input_text, expected):
    assert normalize_temperatures(input_text) == expected


@pytest.mark.parametrize("input_text,expected", [
    ("180 degrees C", "180°C"),
    ("100 degrees C", "100°C"),
    ("0 degrees C", "0°C"),
])
def test_celsius_normalization(input_text, expected):
    assert normalize_temperatures(input_text) == expected


@pytest.mark.parametrize("input_text,expected", [
    (
        "Bake at 350 degrees F and then reduce to 180 degrees C",
        "Bake at 350°F and then reduce to 180°C"
    ),
    (
        "Start with 212 degrees F and cool to 0 degrees C",
        "Start with 212°F and cool to 0°C"
    ),
])
def test_mixed_temperatures(input_text, expected):
    assert normalize_temperatures(input_text) == expected


@pytest.mark.parametrize("input_text,expected", [
    # No temperatures to normalize
    ("No temperature mentioned", "No temperature mentioned"),
    # Missing unit specification
    ("100 degrees", "100 degrees"),
    # Already normalized
    ("350°F and 180°C", "350°F and 180°C"),
])
def test_no_normalization_needed(input_text, expected):
    assert normalize_temperatures(input_text) == expected


@pytest.mark.parametrize("input_text,expected", [
    # Full word "Fahrenheit" instead of "F"
    ("100 degrees Fahrenheit", "100 degrees Fahrenheit"),
    # Misspelled "Celsius"
    ("100 degrees Celcius", "100 degrees Celcius"),
])
def test_partial_matches(input_text, expected):
    assert normalize_temperatures(input_text) == expected


@pytest.mark.parametrize("input_text,expected", [
    # Zero temperature
    ("0 degrees F", "0°F"),
    # Negative temperature
    ("-10 degrees C", "-10°C"),
])
def test_edge_cases(input_text, expected):
    assert normalize_temperatures(input_text) == expected
