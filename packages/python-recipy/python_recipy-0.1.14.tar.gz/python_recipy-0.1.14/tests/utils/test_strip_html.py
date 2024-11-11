import pytest
from recipy.utils import strip_html


@pytest.mark.parametrize("html,expected", [
    ("<p>Hello world</p>", "Hello world"),
    ("<div>Text</div> with <span>HTML</span> tags", "Text with HTML tags"),
    ("<b>Bold</b> and <i>Italic</i>", "Bold and Italic"),
])
def test_basic_html_removal(html, expected):
    assert strip_html(html) == expected


@pytest.mark.parametrize("html,expected", [
    ("<div><p>Nested <span>HTML</span> tags</p></div>", "Nested HTML tags"),
    ("<ul><li>Item 1</li><li>Item 2</li></ul>", "Item 1Item 2"),
])
def test_nested_html_tags(html, expected):
    assert strip_html(html) == expected


@pytest.mark.parametrize("html,expected", [
    ('<a href="https://example.com">Link</a>', "Link"),
    ('<img src="image.jpg" alt="Image">', ""),
])
def test_html_with_attributes(html, expected):
    assert strip_html(html) == expected


@pytest.mark.parametrize("html,expected", [
    ("<div></div>", ""),
    ("<p><span></span></p>", ""),
])
def test_empty_html_tags(html, expected):
    assert strip_html(html) == expected


@pytest.mark.parametrize("text,expected", [
    ("Just plain text", "Just plain text"),
    ("Another line of text", "Another line of text"),
])
def test_no_html_tags(text, expected):
    assert strip_html(text) == expected


@pytest.mark.parametrize("html,expected", [
    ("<p>Unclosed tag", "Unclosed tag"),
    ("Some <b>bold text", "Some bold text"),
    ("Malformed <div><p>HTML", "Malformed HTML"),
])
def test_malformed_html(html, expected):
    assert strip_html(html) == expected
