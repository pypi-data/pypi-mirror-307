import pytest
from recipy.utils import normalize_fractions


@pytest.mark.parametrize("input_text,expected", [
    ("½", "1⁄2"),
    ("¼", "1⁄4"),
    ("¾", "3⁄4"),
    ("⅓", "1⁄3"),
    ("⅔", "2⁄3"),
    ("⅛", "1⁄8"),
    ("⅜", "3⁄8"),
    ("⅝", "5⁄8"),
    ("⅞", "7⁄8"),
])
def test_unicode_fraction_to_ascii(input_text, expected):
    assert normalize_fractions(input_text) == expected


@pytest.mark.parametrize("input_text,expected", [
    ("1 1/2", "1 1⁄2"),
    ("2 1/4", "2 1⁄4"),
    ("3 3/4", "3 3⁄4"),
    ("4 2/3", "4 2⁄3"),
])
def test_mixed_numbers(input_text, expected):
    assert normalize_fractions(input_text) == expected


@pytest.mark.parametrize("input_text,expected", [
    ("0.5", "1⁄2"),
    ("0.25", "1⁄4"),
    ("0.75", "3⁄4"),
    ("0.333", "1⁄3"),
    ("0.666", "2⁄3"),
    ("0.125", "1⁄8"),
    ("0.375", "3⁄8"),
    ("0.625", "5⁄8"),
    ("0.875", "7⁄8"),
])
def test_decimal_to_fraction(input_text, expected):
    assert normalize_fractions(input_text) == expected


@pytest.mark.parametrize("input_text,expected", [
    ("1/2", "1⁄2"),
    ("1/4", "1⁄4"),
    ("3/4", "3⁄4"),
    ("1/3", "1⁄3"),
    ("2/3", "2⁄3"),
    ("1/8", "1⁄8"),
    ("3/8", "3⁄8"),
    ("5/8", "5⁄8"),
    ("7/8", "7⁄8"),
])
def test_fraction_to_decimal(input_text, expected):
    assert normalize_fractions(input_text) == expected


@pytest.mark.parametrize("input_text,expected", [
    ("1 0.5", "1 1⁄2"),
    ("2 0.25", "2 1⁄4"),
    ("3 0.75", "3 3⁄4"),
    ("4 0.333", "4 1⁄3"),
    ("5 0.666", "5 2⁄3"),
    ("6 0.125", "6 1⁄8"),
    ("7 0.375", "7 3⁄8"),
    ("8 0.625", "8 5⁄8"),
    ("9 0.875", "9 7⁄8"),
])
def test_mixed_numbers_with_decimal_conversion(input_text, expected):
    assert normalize_fractions(input_text) == expected


@pytest.mark.parametrize("input_text,expected", [
    ("", ""),
    ("No fractions here", "No fractions here"),
    ("1.5 cups of sugar", "1 1⁄2 cups of sugar"),
    ("¼ cup", "1⁄4 cup"),
    ("1 1/2 cups", "1 1⁄2 cups"),
    ("Some text ½ more text", "Some text 1⁄2 more text"),
])
def test_edge_cases(input_text, expected):
    assert normalize_fractions(input_text) == expected


@pytest.mark.parametrize("input_text,expected", [
    ("1 1/0", "1 1/0"),      # Invalid fraction (division by zero)
    ("1.1.1", "1.1.1"),      # Invalid decimal
])
def test_invalid_input(input_text, expected):
    assert normalize_fractions(input_text) == expected
