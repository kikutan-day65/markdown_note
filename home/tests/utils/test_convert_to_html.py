from unittest.mock import patch

from home.utils.content_utils import convert_to_html


def test_returns_html_content():
    markdown_input = "# Test Markdown"
    html_content = convert_to_html(markdown_input)

    assert "<h1>" in html_content
    assert "Test Markdown" in html_content
    assert "</h1>" in html_content


@patch("home.utils.content_utils.sanitize_content")
def test_calls_sanitize_content(mock_sanitize_content):
    markdown_input = "# Test Markdown"
    convert_to_html(markdown_input)

    mock_sanitize_content.assert_called_once()
