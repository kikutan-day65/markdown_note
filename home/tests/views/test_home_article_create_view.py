from unittest.mock import patch

import pytest
from django.contrib.messages import get_messages
from django.urls import reverse

from home.messages import ARTICLE_CREATE_SUCCESS
from home.models import Article


@pytest.mark.django_db
def test_renders_template(authenticated_client):
    endpoint = reverse("home:article_create")
    response = authenticated_client.get(endpoint)
    template_names = [
        template.name for template in response.templates if template.name is not None
    ]

    assert response.status_code == 200
    assert "home/article_form.html" in template_names


@pytest.mark.django_db
def test_is_update_false_in_context(authenticated_client):
    endpoint = reverse("home:article_create")
    response = authenticated_client.get(endpoint)

    assert response.status_code == 200
    assert response.context["is_update"] is False


@pytest.mark.django_db
def test_post_creates_article_instance(authenticated_client, article_form_data, user):
    endpoint = reverse("home:article_create")
    response = authenticated_client.post(endpoint, data=article_form_data)

    assert response.status_code == 302
    assert Article.objects.count() == 1

    article = Article.objects.first()

    assert article is not None
    assert article.title == article_form_data["title"]
    assert article.markdown_content == article_form_data["markdown_content"]
    assert article.html_content is not None
    assert article.created_at is not None
    assert article.modified_at is None
    assert article.user == user


@pytest.mark.django_db
@patch("home.views.delete_unused_images")
@patch("home.views.associate_images_with_article")
@patch("home.views.convert_to_html")
def test_calls_helper_functions(
    mock_convert_to_html,
    mock_associate_images_with_article,
    mock_delete_unused_images,
    authenticated_client,
    article_form_data,
):
    mock_convert_to_html.return_value = "<p>converted</p>"

    endpoint = reverse("home:article_create")
    response = authenticated_client.post(endpoint, data=article_form_data)

    assert response.status_code == 302
    mock_convert_to_html.assert_called_once()
    mock_associate_images_with_article.assert_called_once()
    mock_delete_unused_images.assert_called_once()


@pytest.mark.django_db
def test_redirects_to_success_url(authenticated_client, article_form_data):
    endpoint = reverse("home:article_create")
    response = authenticated_client.post(endpoint, data=article_form_data)
    redirect_url = reverse("home:home_page")

    assert response.status_code == 302
    assert response.url == redirect_url


@pytest.mark.django_db
def test_shows_success_message(authenticated_client, article_form_data):
    endpoint = reverse("home:article_create")
    response = authenticated_client.post(endpoint, data=article_form_data, follow=True)
    success_messages = list(response.context["messages"])

    assert response.status_code == 200
    assert any(ARTICLE_CREATE_SUCCESS in str(message) for message in success_messages)


@pytest.mark.django_db
def test_get_by_unauthenticated_user(client):
    endpoint = reverse("home:article_create")
    response = client.get(endpoint)
    login_url = reverse("user:login")
    redirect_url = f"{login_url}?next={endpoint}"

    assert response.status_code == 302
    assert response.url == redirect_url


@pytest.mark.django_db
def test_post_by_unauthenticated_user(client, article_form_data):
    endpoint = reverse("home:article_create")
    response = client.post(endpoint, data=article_form_data)
    login_url = reverse("user:login")
    redirect_url = f"{login_url}?next={endpoint}"

    assert response.status_code == 302
    assert response.url == redirect_url


@pytest.mark.django_db
@pytest.mark.parametrize(
    "missing_field, form_data",
    [
        ("title", {"title": "", "markdown_content": "test markdown content"}),
        ("markdown_content", {"title": "Test Title", "markdown_content": ""}),
    ],
    ids=["title", "markdown_content"],
)
def test_missing_required_fields(authenticated_client, missing_field, form_data):
    endpoint = reverse("home:article_create")
    response = authenticated_client.post(endpoint, data=form_data)
    error_messages = list(get_messages(response.wsgi_request))

    assert response.status_code == 200
    assert any(missing_field in str(message) for message in error_messages)
