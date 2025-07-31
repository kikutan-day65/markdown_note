import pytest

from home.utils.content_utils import extract_image_paths


def test_extract_valid_image_path():
    image_path = "article_images/1/20250724/abcdef1234567890abcdef1234567890.jpg"
    content = f'<img src="/media/{image_path}">'
    path_list = extract_image_paths(content)

    assert len(path_list) == 1
    assert path_list == [image_path]


def test_ignore_path_not_expected_pattern():
    image_path = "article_images/1/20250724/unexpected_pattern.jpg"
    content = f'<img src="/media/{image_path}">'
    path_list = extract_image_paths(content)

    assert len(path_list) == 0
    assert path_list == []


def test_returns_empty_list_when_not_contain_img_tag():
    content = "<h1>No img tag</h1>"
    path_list = extract_image_paths(content)

    assert len(path_list) == 0
    assert path_list == []
