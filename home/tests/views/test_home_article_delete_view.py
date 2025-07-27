import pytest
from django.urls import reverse

from home.messages import ARTICLE_DELETE_SUCCESS
from home.models import Article


@pytest.mark.django_db
def test_renders_template(authenticated_client, article):
    endpoint = reverse("home:article_delete", kwargs={"pk": article.pk})
    response = authenticated_client.get(endpoint)
    template_names = [
        template.name for template in response.templates if template.name is not None
    ]

    assert response.status_code == 200
    assert "common/delete.html" in template_names


@pytest.mark.django_db
def test_deletes_article(authenticated_client, article):
    endpoint = reverse("home:article_delete", kwargs={"pk": article.pk})
    response = authenticated_client.post(endpoint)

    assert response.status_code == 302
    assert not Article.objects.filter(pk=article.pk).exists()


@pytest.mark.django_db
def test_redirects_success_url(authenticated_client, article):
    endpoint = reverse("home:article_delete", kwargs={"pk": article.pk})
    response = authenticated_client.post(endpoint)
    redirect_url = reverse("home:home_page")

    assert response.status_code == 302
    assert response.url == redirect_url


@pytest.mark.django_db
def test_shows_success_messages(authenticated_client, article):
    endpoint = reverse("home:article_delete", kwargs={"pk": article.pk})
    response = authenticated_client.post(endpoint, follow=True)
    success_messages = list(response.context["messages"])

    assert response.status_code == 200
    assert any(ARTICLE_DELETE_SUCCESS in str(message) for message in success_messages)


@pytest.mark.django_db
def test_get_by_unauthenticated_user(client, article):
    endpoint = reverse("home:article_delete", kwargs={"pk": article.pk})
    response = client.get(endpoint)
    login_url = reverse("user:login")
    redirect_url = f"{login_url}?next={endpoint}"

    assert response.status_code == 302
    assert response.url == redirect_url


@pytest.mark.django_db
def test_post_by_unauthenticated_user(client, article):
    endpoint = reverse("home:article_delete", kwargs={"pk": article.pk})
    response = client.post(endpoint)
    login_url = reverse("user:login")
    redirect_url = f"{login_url}?next={endpoint}"

    assert response.status_code == 302
    assert response.url == redirect_url


@pytest.mark.django_db
def test_get_deletes_others_article(authenticated_client, another_user):
    # User tries to access other's article delete page
    another_article = Article.objects.create(
        title="Another Title", markdown_content="Another Content", user=another_user
    )
    endpoint = reverse("home:article_delete", kwargs={"pk": another_article.pk})
    response = authenticated_client.get(endpoint)

    assert response.status_code == 404


@pytest.mark.django_db
def test_post_deletes_others_article(
    authenticated_client, article_form_data, another_user
):
    # User tries to delete other's article
    another_article = Article.objects.create(
        title="Another Title", markdown_content="Another Content", user=another_user
    )
    endpoint = reverse("home:article_delete", kwargs={"pk": another_article.pk})
    response = authenticated_client.post(endpoint, data=article_form_data)

    assert response.status_code == 404
