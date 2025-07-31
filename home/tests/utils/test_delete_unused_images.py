from unittest.mock import patch

import pytest

from home.models import ArticleImage
from home.utils.content_utils import delete_unused_images


@pytest.mark.django_db
def test_deletes_article_image_with_none_article(article):
    image_path = "article_images/1/20250724/abcdef1234567890abcdef1234567890.jpg"
    image = ArticleImage.objects.create(
        article_image=image_path,
        article=None,
        user=article.user,
    )
    article.markdown_content = f'<img src="/media/{image_path}">'

    delete_unused_images(article.markdown_content, article)

    assert not ArticleImage.objects.filter(pk=image.pk).exists()


@pytest.mark.django_db
def test_deletes_image_not_used_in_current_content(article):
    image_path = "article_images/1/20250724/abcdef1234567890abcdef1234567890.jpg"
    image = ArticleImage.objects.create(
        article_image=image_path,
        article=article,
        user=article.user,
    )
    article.markdown_content = "<p>no image used here</p>"

    delete_unused_images(article.markdown_content, article)

    assert not ArticleImage.objects.filter(pk=image.pk).exists()


@pytest.mark.django_db
@patch("home.utils.content_utils.extract_image_paths")
def test_calls_extract_image_paths(mock_extract_image_paths, article):
    content = "<p>dummy content</p>"
    mock_extract_image_paths.return_value

    delete_unused_images(content, article)

    mock_extract_image_paths.assert_called_once_with(content)


@pytest.mark.django_db
def test_does_not_delete_image_used_in_content(article):
    image_path = "article_images/1/20250724/abcdef1234567890abcdef1234567890.jpg"
    image = ArticleImage.objects.create(
        article_image=image_path,
        article=article,
        user=article.user,
    )
    content = f'<img src="/media/{image_path}">'

    delete_unused_images(content, article)

    assert ArticleImage.objects.filter(pk=image.pk).exists()


@pytest.mark.django_db
def test_does_not_delete_image_of_other_user(article, another_user):
    image_path = "article_images/99/20250724/abcdef1234567890abcdef1234567890.jpg"

    image = ArticleImage.objects.create(
        article_image=image_path,
        article=None,
        user=another_user,
    )

    content = "<p>No image used</p>"
    delete_unused_images(content, article)

    assert ArticleImage.objects.filter(pk=image.pk).exists()
