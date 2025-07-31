from home.utils.content_utils import sanitize_content


def test_allows_allowed_tags_attributes_and_urls():
    content = (
        "<div class='test-class'><p>text</p><a href='https://examle.com'>link</a></div>"
    )
    clean_html = sanitize_content(content)

    assert "<div" in clean_html
    assert "</div>" in clean_html
    assert 'class="test-class"' in clean_html

    assert "<p>" in clean_html
    assert "</p>" in clean_html
    assert "<a" in clean_html

    assert "</a>" in clean_html
    assert 'href="https://examle.com"' in clean_html
    assert "link" in clean_html


def test_removes_disallowed_tags():
    content = "<p>safe<script>alert('xss')</script></p>"
    clean_html = sanitize_content(content)

    assert "<script>" not in clean_html
    assert "</script>" not in clean_html
    assert "alert" not in clean_html


def test_removes_onclick_attribute():
    content = "<a href='https://example.com' onclick='alert(1)'>link</a>"
    clean_html = sanitize_content(content)

    assert "onclick" not in clean_html


def test_removes_onerror_attribute():
    content = "<img src='x' onerror='alert(1)' />"
    clean_html = sanitize_content(content)

    assert "onerror" not in clean_html


def test_removes_style_attribute():
    content = "<p style='color:red'>Text</p>"
    clean_html = sanitize_content(content)

    assert "style" not in clean_html
