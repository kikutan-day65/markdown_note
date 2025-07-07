from unittest.mock import patch

import pytest
from django.conf import settings
from django.urls import reverse


@pytest.mark.django_db
def test_upload_article_images_success(authenticated_client, test_image):
    endpoint = reverse("home:upload_article_images")
    response = authenticated_client.post(endpoint, {"image": test_image})
    json_data = response.json()

    assert response.status_code == 200
    assert json_data["success"] is True
    assert "url" in json_data


@pytest.mark.django_db
def test_upload_article_image_uses_storage_backend(authenticated_client, test_image):
    endpoint = reverse("home:upload_article_images")

    with patch("home.views.default_storage.save") as mock_save:
        mock_save.return_value = "dummy/path/test_image.jpg"
        response = authenticated_client.post(endpoint, {"image": test_image})

        assert response.status_code == 200
        mock_save.assert_called_once()


@pytest.mark.django_db
def test_upload_article_images_returns_correct_url(authenticated_client, test_image):
    endpoint = reverse("home:upload_article_images")
    response = authenticated_client.post(endpoint, {"image": test_image})
    json_data = response.json()

    assert json_data["url"].startswith(settings.MEDIA_URL)


@pytest.mark.django_db
def test_upload_article_images_post_without_image_fails(authenticated_client):
    endpoint = reverse("home:upload_article_images")
    response = authenticated_client.post(endpoint, {})
    json_data = response.json()

    assert response.status_code == 400
    assert json_data["success"] is False
    assert "error" in json_data
    assert json_data["error"] == "No image uploaded"
