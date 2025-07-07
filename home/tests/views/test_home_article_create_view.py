import pytest
from django.contrib.messages import get_messages
from django.urls import reverse

from home.messages import ARTICLE_CREATE_SUCCESS


@pytest.mark.django_db
def test_article_create_view_renders_successfully(authenticated_client):
    endpoint = reverse("home:article_create")
    response = authenticated_client.get(endpoint)

    assert response.status_code == 200
    assert "home/article_form.html" in [t.name for t in response.templates]


import pytest
from django.urls import reverse

from home.models import Article


@pytest.mark.django_db
def test_article_create_view_with_valid_data(authenticated_client, test_user):
    form_data = {
        "title": "test_title",
        "content": "test_content",
    }
    endpoint = reverse("home:article_create")
    success_endpoint = reverse("home:home_page")
    response = authenticated_client.post(endpoint, data=form_data)

    assert response.status_code == 302
    assert response.url == success_endpoint

    article = Article.objects.get(title="test_title")
    assert article.content == "test_content"
    assert article.user == test_user


@pytest.mark.django_db
def test_article_create_view_shows_success_message(authenticated_client):
    form_data = {
        "title": "test_title",
        "content": "test_content",
    }
    endpoint = reverse("home:article_create")
    response = authenticated_client.post(endpoint, data=form_data)
    messages = list(get_messages(response.wsgi_request))

    assert any(ARTICLE_CREATE_SUCCESS in str(m) for m in messages)


@pytest.mark.django_db
def test_article_create_view_contains_is_update_in_context(authenticated_client):
    endpoint = reverse("home:article_create")
    response = authenticated_client.get(endpoint)

    assert "is_update" in response.context
    assert response.context["is_update"] == False


@pytest.mark.django_db
def test_article_create_view_get_by_unauthenticated_user(client):
    endpoint = reverse("home:article_create")
    login_url = reverse("user:login")
    redirect_endpoint = f"{login_url}?next={endpoint}"
    response = client.get(endpoint)

    assert response.status_code == 302
    assert response.url == redirect_endpoint


@pytest.mark.django_db
def test_article_create_view_post_by_unauthenticated_user(client):
    form_data = {"title": "test_title", "content": "test_content"}
    endpoint = reverse("home:article_create")
    login_url = reverse("user:login")
    redirect_endpoint = f"{login_url}?next={endpoint}"
    response = client.post(endpoint, data=form_data)

    assert response.status_code == 302
    assert response.url == redirect_endpoint


@pytest.mark.django_db
@pytest.mark.parametrize(
    "error_field, form_data",
    [
        ("title", {"title": "", "content": "test_content"}),
        ("content", {"title": "test_title", "content": ""}),
    ],
    ids=["missing_title", "missing_content"],
)
def test_article_create_view_without_required_fields(
    authenticated_client, error_field, form_data
):
    endpoint = reverse("home:article_create")
    response = authenticated_client.post(endpoint, data=form_data)

    assert response.status_code == 200
    assert "form" in response.context
    assert error_field in response.context["form"].errors


@pytest.mark.django_db
@pytest.mark.parametrize(
    "form_data",
    [
        {"title": "", "content": "test_content"},
        {"title": "test_title", "content": ""},
    ],
    ids=["missing_title", "missing_content"],
)
def test_article_create_view_shows_error_messages(authenticated_client, form_data):
    endpoint = reverse("home:article_create")
    response = authenticated_client.post(endpoint, data=form_data)
    messages = list(get_messages(response.wsgi_request))

    assert messages
