import pytest
from django.core.files.uploadedfile import SimpleUploadedFile

from home.constants import (
    MAX_FILES_PER_USER,
    MAX_IMAGE_SIZE,
    MAX_UNASSOCIATED_FILES_PER_USER,
)
from home.messages import (
    IMAGE_SIZE_ERROR,
    MAX_FILES_ERROR,
    MAX_UNASSOCIATED_FILES_ERROR,
)
from home.models import ArticleImage
from home.utils.content_utils import is_valid_upload


@pytest.mark.django_db
def test_valid_upload_returns_true(user, image):
    is_valid, error = is_valid_upload(user, image)

    assert is_valid is True
    assert error is None


@pytest.mark.django_db
def test_image_too_large_returns_error(user):
    # Create oversized image
    oversized_content = b"x" * (MAX_IMAGE_SIZE + 1)
    oversized_image = SimpleUploadedFile(
        name="oversized.jpg", content=oversized_content, content_type="image/jpeg"
    )

    is_valid, error = is_valid_upload(user, oversized_image)

    assert is_valid is False
    assert error == IMAGE_SIZE_ERROR


@pytest.mark.django_db
def test_too_many_unassociated_images(user):
    # Create unassociated article images
    for _ in range(MAX_UNASSOCIATED_FILES_PER_USER):
        ArticleImage.objects.create(
            article_image="article_images/1/tmp/dummy.jpg",
            article=None,
            user=user,
        )

    dummy_image = SimpleUploadedFile(
        name="new.jpg", content=b"dummy", content_type="image/jpeg"
    )

    is_valid, error = is_valid_upload(user, dummy_image)

    assert is_valid is False
    assert error == MAX_UNASSOCIATED_FILES_ERROR


@pytest.mark.django_db
def test_too_many_total_images(user, article):
    # Create article images
    for i in range(MAX_FILES_PER_USER):
        ArticleImage.objects.create(
            article_image=f"article_images/1/tmp/dummy_{i}.jpg",
            article=article,
            user=user,
        )

    dummy_image = SimpleUploadedFile(
        name="new.jpg", content=b"dummy", content_type="image/jpeg"
    )

    is_valid, error = is_valid_upload(user, dummy_image)

    assert is_valid is False
    assert error == MAX_FILES_ERROR
