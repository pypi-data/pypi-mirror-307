import pytest
from recipy.utils import collapse_whitespace


@pytest.mark.parametrize("input_text,expected", [
    ("Line 1\nLine 2", "Line 1 Line 2"),
    ("Line 1\rLine 2", "Line 1 Line 2"),
    ("Line 1\n\rLine 2", "Line 1 Line 2"),
])
def test_collapse_newlines(input_text, expected):
    assert collapse_whitespace(input_text) == expected


@pytest.mark.parametrize("input_text,expected", [
    ("Tabbed\ttext", "Tabbed text"),
    ("Multiple\ttabs\tin\ttext", "Multiple tabs in text"),
])
def test_collapse_tabs(input_text, expected):
    assert collapse_whitespace(input_text) == expected


@pytest.mark.parametrize("input_text,expected", [
    ("Single    space", "Single space"),
    ("   Leading and trailing spaces   ", "Leading and trailing spaces"),
])
def test_collapse_spaces(input_text, expected):
    assert collapse_whitespace(input_text) == expected


@pytest.mark.parametrize("input_text,expected", [
    ("Mixed \n \r \t whitespace text", "Mixed whitespace text"),
    ("\tText \nwith \rvarious \t\n\rwhitespace", "Text with various whitespace"),
])
def test_collapse_mixed_whitespace(input_text, expected):
    assert collapse_whitespace(input_text) == expected


def test_zero_width_space():
    input_text = "Text\u200Bwith\u200Bzero\u200Bwidth\u200Bspace"
    expected = "Text with zero width space"
    assert collapse_whitespace(input_text) == expected


def test_non_breaking_space():
    input_text = "Text\xA0with\xA0non\xA0breaking\xA0space"
    expected = "Text with non breaking space"
    assert collapse_whitespace(input_text) == expected


@pytest.mark.parametrize("input_text,expected", [
    ("", ""),
    ("No changes needed", "No changes needed"),
])
def test_edge_cases(input_text, expected):
    assert collapse_whitespace(input_text) == expected