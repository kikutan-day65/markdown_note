from unittest.mock import patch

import pytest
from django.urls import reverse

from home.messages import IMAGE_NOT_UPLOADED, LOGIN_REQUIRED
from home.models import ArticleImage


@pytest.mark.django_db
def test_upload_image(authenticated_client, image):
    endpoint = reverse("home:upload_article_images")
    response = authenticated_client.post(endpoint, data={"image": image})

    assert response.status_code == 200

    json_data = response.json()
    assert json_data["image_url"]


@pytest.mark.django_db
def test_creates_article_image_instance(authenticated_client, image, user):
    endpoint = reverse("home:upload_article_images")
    response = authenticated_client.post(endpoint, data={"image": image})

    assert response.status_code == 200
    assert ArticleImage.objects.count() == 1

    article_image = ArticleImage.objects.first()

    assert article_image.article is None
    assert article_image.user == user


@pytest.mark.django_db
@patch("home.views.is_valid_upload")
def test_creates_article_image_instance(
    mock_is_valid_upload, authenticated_client, image
):
    mock_is_valid_upload.return_value = (True, "")

    endpoint = reverse("home:upload_article_images")
    response = authenticated_client.post(endpoint, data={"image": image})

    assert response.status_code == 200
    mock_is_valid_upload.assert_called_once()


@pytest.mark.django_db
def test_upload_image_by_unauthenticated_user(client, image):
    endpoint = reverse("home:upload_article_images")
    response = client.post(endpoint, data={"image": image})

    assert response.status_code == 403

    json_data = response.json()
    assert json_data["success"] is False
    assert json_data["error"] == LOGIN_REQUIRED


@pytest.mark.django_db
def test_post_without_image(authenticated_client):
    endpoint = reverse("home:upload_article_images")
    response = authenticated_client.post(endpoint)

    assert response.status_code == 400

    json_data = response.json()
    assert json_data["error"] == IMAGE_NOT_UPLOADED
