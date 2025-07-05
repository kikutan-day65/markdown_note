from unittest.mock import patch

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import IntegrityError
from django.utils import timezone

from home.models import ArticleImage


@pytest.mark.django_db
def test_create_article_image(test_article, test_image):
    article_image = ArticleImage.objects.create(
        article_image=test_image, article=test_article
    )

    assert article_image.pk is not None
    assert article_image.article == test_article


@pytest.mark.django_db
def test_uploaded_at_is_set_automatically(test_article, test_image):
    before = timezone.now()
    article_image = ArticleImage.objects.create(
        article_image=test_image, article=test_article
    )
    after = timezone.now()

    assert before < article_image.uploaded_at < after


@pytest.mark.django_db
def test_user_can_access_related_article_images(test_article):
    img1 = SimpleUploadedFile("img1.jpg", b"img1-content", content_type="image/jpeg")
    img2 = SimpleUploadedFile("img2.jpg", b"img2-content", content_type="image/jpeg")

    ArticleImage.objects.create(article=test_article, article_image=img1)
    ArticleImage.objects.create(article=test_article, article_image=img2)
    images = test_article.images.all()
    filenames = [img.article_image.name for img in images]

    assert images.count() == 2
    assert any("img1" in name for name in filenames)
    assert any("img2" in name for name in filenames)
