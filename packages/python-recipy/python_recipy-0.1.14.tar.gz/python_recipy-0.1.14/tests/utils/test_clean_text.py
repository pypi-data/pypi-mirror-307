import pytest
from recipy.utils import clean_text


def test_empty_string():
    assert clean_text("") == ""


@pytest.mark.parametrize("input_text,expected", [
    ("Tom &amp; Jerry", "Tom & Jerry"),
    ("Bake at 350 degrees F for 30 minutes", "Bake at 350°F for 30 minutes"),
    ("Add 1/2 cup of sugar", "Add 1⁄2 cup of sugar"),
])
def test_basic_cleaning(input_text, expected):
    assert clean_text(input_text) == expected


@pytest.mark.parametrize("input_text,expected", [
    ("  350 degrees F   &amp;  1/2 tsp salt  ", "350°F & 1⁄2 tsp salt"),
    ("180 degrees C and ¾ cup milk", "180°C and 3⁄4 cup milk"),
])
def test_combined_operations(input_text, expected):
    assert clean_text(input_text) == expected


@pytest.mark.parametrize("input_text,expected", [
    ("   Leading and trailing spaces   ", "Leading and trailing spaces"),
    ("Multiple    spaces    collapsed", "Multiple spaces collapsed"),
    ("Newline\nand\ttab handling", "Newline and tab handling"),
])
def test_whitespace_handling(input_text, expected):
    assert clean_text(input_text) == expected


@pytest.mark.parametrize("input_text,expected", [
    ("1/2 cup of sugar &amp; 3/4 tsp salt", "1⁄2 cup of sugar & 3⁄4 tsp salt"),
    ("Mix 2/3 cup flour", "Mix 2⁄3 cup flour"),
])
def test_html_entities_and_fractions(input_text, expected):
    assert clean_text(input_text) == expected


@pytest.mark.parametrize("input_text,expected", [
    ("0 degrees F", "0°F"),
    ("-10 degrees C and 1/8 tsp", "-10°C and 1⁄8 tsp"),
    ("No temperature or fraction", "No temperature or fraction"),
])
def test_edge_cases(input_text, expected):
    assert clean_text(input_text) == expected


def test_invalid_fraction():
    assert clean_text("Invalid fraction 1/0") == "Invalid fraction 1/0"
