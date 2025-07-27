import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_renders_template(client, article):
    endpoint = reverse("home:article_detail", kwargs={"pk": article.pk})
    response = client.get(endpoint)
    template_names = [
        template.name for template in response.templates if template.name is not None
    ]

    assert response.status_code == 200
    assert "home/article_detail.html" in template_names


@pytest.mark.django_db
def test_includes_article_detail_in_context(client, article):
    endpoint = reverse("home:article_detail", kwargs={"pk": article.pk})
    response = client.get(endpoint)

    assert response.status_code == 200
    assert "article_detail" in response.context


@pytest.mark.django_db
def test_access_to_nonexistent_article(client):
    dummy_pk = 999
    endpoint = reverse("home:article_detail", kwargs={"pk": dummy_pk})
    response = client.get(endpoint)

    assert response.status_code == 404
