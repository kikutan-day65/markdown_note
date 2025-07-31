from unittest.mock import patch

import pytest

from home.models import ArticleImage
from home.utils.content_utils import associate_images_with_article


@pytest.mark.django_db
def test_associate_images_with_article_id(article):
    image_path = f"article_images/{article.user.id}/20250724/0ca4923546bb42beac17b7fe6b30ebf2.png"
    image = ArticleImage.objects.create(
        article_image=image_path,
        article=None,
        user=article.user,
    )

    content = f'<img alt="alt text" src="/media/{image_path}">'
    associate_images_with_article(content, article)

    image.refresh_from_db()
    assert image.article == article
    assert image.article_image == image_path
    assert image.user == article.user


@patch("home.utils.content_utils.extract_image_paths")
def test_calls_extract_image_paths(mock_extract_image_paths, article):
    content = "<h1>test_content</h1>"
    associate_images_with_article(content, article)

    mock_extract_image_paths.assert_called_once()
