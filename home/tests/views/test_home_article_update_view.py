from unittest.mock import patch

import pytest
from django.contrib.messages import get_messages
from django.urls import reverse

from home.messages import ARTICLE_UPDATE_SUCCESS
from home.models import Article


@pytest.mark.django_db
def test_renders_template(authenticated_client, article):
    endpoint = reverse("home:article_update", kwargs={"pk": article.pk})
    response = authenticated_client.get(endpoint)
    template_names = [
        template.name for template in response.templates if template.name is not None
    ]

    assert response.status_code == 200
    assert "home/article_form.html" in template_names


@pytest.mark.django_db
def test_is_update_true_in_context(authenticated_client, article):
    endpoint = reverse("home:article_update", kwargs={"pk": article.pk})
    response = authenticated_client.get(endpoint)

    assert response.status_code == 200
    assert response.context["is_update"] is True


@pytest.mark.django_db
def test_post_updates_article_instance(
    authenticated_client, article, article_form_data, user
):
    endpoint = reverse("home:article_update", kwargs={"pk": article.pk})
    response = authenticated_client.post(endpoint, data=article_form_data)

    article.refresh_from_db()

    assert response.status_code == 302
    assert Article.objects.count() == 1
    assert article is not None
    assert article.title == article_form_data["title"]
    assert article.markdown_content == article_form_data["markdown_content"]
    assert article.html_content is not None
    assert article.created_at is not None
    assert article.modified_at is not None
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
    article,
    article_form_data,
):
    mock_convert_to_html.return_value = "<p>converted</p>"

    endpoint = reverse("home:article_update", kwargs={"pk": article.pk})
    response = authenticated_client.post(endpoint, data=article_form_data)

    assert response.status_code == 302
    mock_convert_to_html.assert_called_once()
    mock_associate_images_with_article.assert_called_once()
    mock_delete_unused_images.assert_called_once()


@pytest.mark.django_db
def test_redirects_to_success_url(authenticated_client, article, article_form_data):
    endpoint = reverse("home:article_update", kwargs={"pk": article.pk})
    response = authenticated_client.post(endpoint, data=article_form_data)

    assert response.status_code == 302
    assert response.url == reverse("home:article_detail", kwargs={"pk": article.pk})


@pytest.mark.django_db
def test_shows_success_message(authenticated_client, article, article_form_data):
    endpoint = reverse("home:article_update", kwargs={"pk": article.pk})
    response = authenticated_client.post(endpoint, data=article_form_data, follow=True)
    success_messages = list(response.context["messages"])

    assert response.status_code == 200
    assert any(ARTICLE_UPDATE_SUCCESS in str(message) for message in success_messages)


@pytest.mark.django_db
def test_get_updates_others_article(authenticated_client, another_user):
    # User tries to access other's article update page
    another_article = Article.objects.create(
        title="Another Title", markdown_content="Another Content", user=another_user
    )
    endpoint = reverse("home:article_update", kwargs={"pk": another_article.pk})
    response = authenticated_client.get(endpoint)

    assert response.status_code == 404


@pytest.mark.django_db
def test_post_updates_others_article(authenticated_client, article_form_data, another_user):
    # User tries to update other's article
    another_article = Article.objects.create(
        title="Another Title", markdown_content="Another Content", user=another_user
    )
    endpoint = reverse("home:article_update", kwargs={"pk": another_article.pk})
    response = authenticated_client.post(endpoint, data=article_form_data)

    assert response.status_code == 404


@pytest.mark.django_db
def test_get_by_unauthenticated_user(client, article):
    endpoint = reverse("home:article_update", kwargs={"pk": article.pk})
    response = client.get(endpoint)
    login_url = reverse("user:login")
    redirect_url = f"{login_url}?next={endpoint}"

    assert response.status_code == 302
    assert response.url == redirect_url


@pytest.mark.django_db
def test_post_by_unauthenticated_user(client, article, article_form_data):
    endpoint = reverse("home:article_update", kwargs={"pk": article.pk})
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
def test_missing_required_fields(
    authenticated_client, article, missing_field, form_data
):
    endpoint = reverse("home:article_update", kwargs={"pk": article.pk})
    response = authenticated_client.post(endpoint, data=form_data)
    error_messages = list(get_messages(response.wsgi_request))

    assert response.status_code == 200
    assert any(missing_field in str(message) for message in error_messages)
