import html
import re
from fractions import Fraction
from typing import Optional

import nh3


def clean_text(text: str) -> str:
    """
    Clean the input text by unescaping HTML entities, normalizing fractions and temperatures,
    collapsing whitespace, and stripping leading and trailing spaces.

    :param text: The input text to be cleaned
    :type text: str
    :returns: The cleaned text
    :rtype: str
    """
    if text:
        text = html.unescape(text)
        text = normalize_fractions(text)
        text = normalize_temperatures(text)
        text = collapse_whitespace(text)
        text = text.strip()
    return text


def strip_html(text: str) -> str:
    """
    Strip all HTML tags from the input text using nh3, allowing no tags.

    :param text: The input text with potential HTML content
    :type text: str
    :returns: The text with HTML tags removed
    :rtype: str
    """
    return nh3.clean(text, tags=set())


def collapse_whitespace(val: str) -> str:
    """
    Replace various whitespace characters (newlines, tabs, etc.) with a space, and collapse multiple
    spaces into a single space.

    :param val: The input text with potential excessive whitespace
    :type val: str
    :returns: The text with collapsed whitespace
    :rtype: str
    """
    val = re.sub(r'[\n\r\u200B\t\xA0\s]', ' ', val)
    val = re.sub(r'\s{2,}', ' ', val)
    val = val.strip()
    return val


def parse_time(val: str) -> Optional[int]:
    """
    Parse an ISO 8601 duration string (e.g., 'PT2H30M') and convert it to total minutes.

    :param val: The ISO 8601 duration string
    :type val: str
    :returns: The total duration in minutes, or None if the input is invalid
    :rtype: Optional[int]
    """
    if not val or val.isspace():
        return None

    match = re.match(r'PT(?:(\d+)H)?(?:(\d+)M)?$', val)

    if not match:
        return None

    # If neither hours nor minutes are provided, return None
    if not match.group(1) and not match.group(2):
        return None

    hours = int(match.group(1)) if match.group(1) else 0
    minutes = int(match.group(2)) if match.group(2) else 0

    return hours * 60 + minutes


def normalize_temperatures(val: str) -> str:
    """
    Normalize temperature descriptions in the input text, replacing phrases like '350 degrees F'
    with '350°F'.

    :param val: The input text containing temperature descriptions
    :type val: str
    :returns: The text with normalized temperature descriptions
    :rtype: str
    """
    val = re.sub(r'(\d+) degrees F\b', lambda x: f"{int(x.group(1))}°F", val)
    val = re.sub(r'(\d+) degrees C\b', lambda x: f"{int(x.group(1))}°C", val)
    return val


def normalize_fractions(val: str) -> str:
    """
    Normalize fractions in the input text by converting Unicode fractions to ASCII,
    converting fractions to decimals and back to fractions, and replacing '/' with
    the Unicode fraction slash.

    :param val: The input text containing fractions
    :type val: str
    :returns: The text with normalized fractions
    :rtype: str
    """
    val = _unicode_fraction_to_ascii(val)
    try:
        normalized = _fraction_to_decimal(val)
        normalized = _decimal_to_fraction(normalized)
        normalized = re.sub(r'(\d+)/(\d+)', r'\1⁄\2', normalized)
        return normalized
    except ZeroDivisionError:
        return val


def _unicode_fraction_to_ascii(val):
    fractions = {
        "¼": "1/4",
        "⅓": "1/3",
        "½": "1/2",
        "⅖": "2/5",
        "⅗": "3/5",
        "⅘": "4/5",
        "⅙": "1/6",
        "⅐": "1/7",
        "⅛": "1/8",
        "⅑": "1/9",
        "⅒": "1/10",
        "⅚": "5/6",
        "⅜": "3/8",
        "⅝": "5/8",
        "⅞": "7/8",
        "¾": "3/4",
        "⅔": "2/3",
        "⅕": "1/5"
    }

    for unicode_frac, ascii_frac in fractions.items():
        val = val.replace(unicode_frac, ascii_frac)

    return val


def _mixed_number(fraction: Fraction) -> str:
    whole = fraction.numerator // fraction.denominator
    remainder = fraction.numerator % fraction.denominator
    if whole == 0:
        return f"{fraction.numerator}/{fraction.denominator}"
    elif remainder == 0:
        return str(whole)
    else:
        return f"{whole} {remainder}/{fraction.denominator}"


def _decimal_to_fraction(val):
    def replace_decimal(match):
        d = match.group(0)
        return _mixed_number(Fraction(d).limit_denominator(8))

    # Split the input into tokens based on spaces or non-numeric characters
    tokens = re.split(r'(\s+|[^0-9.])', val)

    # Process only valid decimal numbers that have a fractional part (i.e., a digit after the decimal point)
    tokens = [re.sub(r'^\d+\.\d+$', replace_decimal, token) for token in tokens]

    return ''.join(tokens)


def _fraction_to_decimal(val):
    def replace_fraction(s):
        i, f = s.groups(0)
        f = Fraction(f)
        return str(int(i) + float(f)) if i else str(float(f))
    return re.sub(r'(?:(\d+)[-\s])?(\d+/\d+)', replace_fraction, val)
