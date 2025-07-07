import pytest
from django.contrib.messages import get_messages
from django.urls import reverse
from django.utils import timezone

from home.messages import ARTICLE_UPDATE_SUCCESS
from home.models import Article


@pytest.mark.django_db
def test_article_update_view_renders_successfully(authenticated_client, test_article):
    endpoint = reverse("home:article_update", kwargs={"pk": test_article.pk})
    response = authenticated_client.get(endpoint)

    assert response.status_code == 200
    assert "home/article_form.html" in [t.name for t in response.templates]


@pytest.mark.django_db
def test_article_update_view_with_valid_data(
    authenticated_client, test_article, test_user
):
    endpoint = reverse("home:article_update", kwargs={"pk": test_article.pk})
    success_endpoint = reverse("home:article_detail", kwargs={"pk": test_article.pk})
    form_data = {"title": "test_title_updated", "content": "test_content_updated"}
    response = authenticated_client.post(endpoint, data=form_data)

    assert response.status_code == 302
    assert response.url == success_endpoint

    article = Article.objects.get(title="test_title_updated")
    assert article.content == "test_content_updated"
    assert article.user == test_user


@pytest.mark.django_db
def test_article_update_view_contains_is_update_in_context(
    authenticated_client, test_article
):
    endpoint = reverse("home:article_update", kwargs={"pk": test_article.pk})
    response = authenticated_client.get(endpoint)

    assert "is_update" in response.context
    assert response.context["is_update"] == True


@pytest.mark.django_db
def test_article_update_view_modified_at_is_set_automatically(
    authenticated_client, test_article
):
    endpoint = reverse("home:article_update", kwargs={"pk": test_article.pk})
    form_data = {"title": "test_title_updated", "content": "test_content_updated"}
    before = timezone.now()
    response = authenticated_client.post(endpoint, data=form_data)
    after = timezone.now()

    test_article.refresh_from_db()
    assert test_article.modified_at is not None
    assert before < test_article.modified_at < after


@pytest.mark.django_db
def test_article_update_view_shows_success_messages(authenticated_client, test_article):
    endpoint = reverse("home:article_update", kwargs={"pk": test_article.pk})
    form_data = {"title": "test_title_updated", "content": "test_content_updated"}
    response = authenticated_client.post(endpoint, data=form_data)
    messages = list(get_messages(response.wsgi_request))

    assert any(ARTICLE_UPDATE_SUCCESS in str(m) for m in messages)


@pytest.mark.django_db
def test_article_update_view_get_by_unauthenticated_user(client, test_article):
    endpoint = reverse("home:article_update", kwargs={"pk": test_article.pk})
    login_url = reverse("user:login")
    redirect_endpoint = f"{login_url}?next={endpoint}"
    response = client.get(endpoint)

    assert response.status_code == 302
    assert response.url == redirect_endpoint


@pytest.mark.django_db
def test_article_update_view_post_by_unauthenticated_user(client, test_article):
    form_data = {"title": "test_title_updated", "content": "test_content_updated"}
    endpoint = reverse("home:article_update", kwargs={"pk": test_article.pk})
    login_url = reverse("user:login")
    redirect_endpoint = f"{login_url}?next={endpoint}"
    response = client.post(endpoint, data=form_data)

    assert response.status_code == 302
    assert response.url == redirect_endpoint


@pytest.mark.django_db
@pytest.mark.parametrize(
    "error_field, form_data",
    [
        ("title", {"title": "", "content": "test_content_updated"}),
        ("content", {"title": "test_title_updated", "content": ""}),
    ],
    ids=["missing_title", "missing_content"],
)
def test_article_update_view_without_required_fields(
    authenticated_client, test_article, error_field, form_data
):
    endpoint = reverse("home:article_update", kwargs={"pk": test_article.pk})
    response = authenticated_client.post(endpoint, data=form_data)

    assert response.status_code == 200
    assert "form" in response.context
    assert error_field in response.context["form"].errors


@pytest.mark.django_db
def test_update_view_get_forbids_access_to_other_users_article(
    authenticated_client, taken_user
):
    other_user_article = Article.objects.create(
        title="other_user_title", content="other_user_content", user=taken_user
    )
    endpoint = reverse("home:article_update", kwargs={"pk": other_user_article.pk})
    response = authenticated_client.get(endpoint)

    assert response.status_code == 404


@pytest.mark.django_db
def test_update_view_post_forbids_access_to_other_users_article(
    authenticated_client, taken_user
):
    other_user_article = Article.objects.create(
        title="other_user_title", content="other_user_content", user=taken_user
    )
    endpoint = reverse("home:article_update", kwargs={"pk": other_user_article.pk})
    form_data = {"title": "updated_title", "content": "updated_content"}
    response = authenticated_client.post(endpoint, data=form_data)

    assert response.status_code == 404
