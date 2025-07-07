import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_home_view_renders_successfully(client, test_article):
    endpoint = reverse("home:article_detail", kwargs={"pk": test_article.pk})
    response = client.get(endpoint)

    assert response.status_code == 200
    assert "home/article_detail.html" in [t.name for t in response.templates]


@pytest.mark.django_db
def test_home_view_contains_article_detail_in_context(client, test_article):
    endpoint = reverse("home:article_detail", kwargs={"pk": test_article.pk})
    response = client.get(endpoint)

    assert "article_detail" in response.context


@pytest.mark.django_db
def test_home_view_contains_article_html_in_context(client, test_article):
    endpoint = reverse("home:article_detail", kwargs={"pk": test_article.pk})
    response = client.get(endpoint)

    assert "article_html" in response.context


@pytest.mark.django_db
def test_article_detail_view_404_when_not_found(client):
    invalid_pk = 9999
    endpoint = reverse("home:article_detail", kwargs={"pk": invalid_pk})
    response = client.get(endpoint)

    assert response.status_code == 404
