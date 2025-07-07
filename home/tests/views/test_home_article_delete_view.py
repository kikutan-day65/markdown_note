import pytest
from django.contrib.messages import get_messages
from django.urls import reverse

from home.messages import ARTICLE_DELETE_SUCCESS
from home.models import Article


@pytest.mark.django_db
def test_article_delete_view_renders_successfully(authenticated_client, test_article):
    endpoint = reverse("home:article_delete", kwargs={"pk": test_article.pk})
    response = authenticated_client.get(endpoint)

    assert response.status_code == 200
    assert "common/delete.html" in [t.name for t in response.templates]


@pytest.mark.django_db
def test_article_delete_view_successfully(authenticated_client, test_article):
    endpoint = reverse("home:article_delete", kwargs={"pk": test_article.pk})
    success_endpoint = reverse("home:home_page")
    response = authenticated_client.post(endpoint)

    with pytest.raises(Article.DoesNotExist):
        Article.objects.get(pk=test_article.pk)

    assert response.status_code == 302
    assert response.url == success_endpoint


@pytest.mark.django_db
def test_article_delete_view_shows_success_message(authenticated_client, test_article):
    endpoint = reverse("home:article_delete", kwargs={"pk": test_article.pk})
    response = authenticated_client.post(endpoint)
    messages = list(get_messages(response.wsgi_request))

    assert any(ARTICLE_DELETE_SUCCESS in str(m) for m in messages)


@pytest.mark.django_db
def test_article_delete_view_get_by_unauthenticated_user(client, test_article):
    endpoint = reverse("home:article_delete", kwargs={"pk": test_article.pk})
    login_url = reverse("user:login")
    redirect_endpoint = f"{login_url}?next={endpoint}"
    response = client.get(endpoint)

    assert response.status_code == 302
    assert response.url == redirect_endpoint


@pytest.mark.django_db
def test_article_delete_view_post_by_unauthenticated_user(client, test_article):
    endpoint = reverse("home:article_delete", kwargs={"pk": test_article.pk})
    login_url = reverse("user:login")
    redirect_endpoint = f"{login_url}?next={endpoint}"
    response = client.post(endpoint)

    assert response.status_code == 302
    assert response.url == redirect_endpoint


@pytest.mark.django_db
def test_delete_view_get_forbids_access_to_other_users_article(
    authenticated_client, taken_user
):
    other_user_article = Article.objects.create(
        title="other_user_title", content="other_user_content", user=taken_user
    )
    endpoint = reverse("home:article_delete", kwargs={"pk": other_user_article.pk})
    response = authenticated_client.get(endpoint)

    assert response.status_code == 404


@pytest.mark.django_db
def test_update_view_post_forbids_access_to_other_users_article(
    authenticated_client, taken_user
):
    other_user_article = Article.objects.create(
        title="other_user_title", content="other_user_content", user=taken_user
    )
    endpoint = reverse("home:article_delete", kwargs={"pk": other_user_article.pk})
    response = authenticated_client.post(endpoint)

    assert response.status_code == 404


@pytest.mark.django_db
def test_article_delete_view_with_invalid_pk_returns_404(authenticated_client):
    invalid_pk = 9999
    endpoint = reverse("home:article_delete", kwargs={"pk": invalid_pk})

    response_get = authenticated_client.get(endpoint)
    assert response_get.status_code == 404

    response_post = authenticated_client.post(endpoint)
    assert response_post.status_code == 404
