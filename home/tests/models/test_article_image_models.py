from unittest.mock import patch

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import IntegrityError
from django.utils import timezone

from home.models import ArticleImage


@pytest.mark.django_db
def test_create_article_image(article, image):
    article_image = ArticleImage.objects.create(
        article_image=image, article=article, user=article.user
    )

    assert article_image.pk is not None
    assert article_image.article == article


@pytest.mark.django_db
def test_uploaded_at_is_set_automatically(article, image):
    before = timezone.now()
    article_image = ArticleImage.objects.create(
        article_image=image, article=article, user=article.user
    )
    after = timezone.now()

    assert before < article_image.uploaded_at < after


@pytest.mark.django_db
def test_user_can_access_related_article_images(article):
    img1 = SimpleUploadedFile("img1.jpg", b"img1-content", content_type="image/jpeg")
    img2 = SimpleUploadedFile("img2.jpg", b"img2-content", content_type="image/jpeg")

    image1 = ArticleImage.objects.create(
        article=article, article_image=img1, user=article.user
    )
    image2 = ArticleImage.objects.create(
        article=article, article_image=img2, user=article.user
    )

    images = article.images.all()

    assert images.count() == 2
    assert set(images) == {image1, image2}


@pytest.mark.django_db
@patch("django.db.models.fields.files.FieldFile.delete")
def test_post_delete_signal_deletes_image_file(mock_delete, article, image):
    article_image = ArticleImage.objects.create(
        article_image=image,
        article=article,
        user=article.user,
    )

    article_image.delete()

    mock_delete.assert_called_once()
