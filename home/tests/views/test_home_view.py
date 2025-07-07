import pytest
from django.urls import reverse

from home.models import Article


@pytest.mark.django_db
def test_home_view_renders_successfully(client):
    endpoint = reverse("home:home_page")
    response = client.get(endpoint)

    assert response.status_code == 200
    assert "home/home.html" in [t.name for t in response.templates]


@pytest.mark.django_db
def test_home_view_contains_articles(client, test_article):
    endpoint = reverse("home:home_page")
    response = client.get(endpoint)

    assert "articles" in response.context
    assert list(response.context["articles"])


@pytest.mark.django_db
def test_home_view_contains_filter_in_context(client, test_article):
    endpoint = reverse("home:home_page")
    response = client.get(endpoint)

    assert "filter" in response.context


@pytest.mark.django_db
def test_home_view_pagination(client, test_user):
    for i in range(11):
        Article.objects.create(
            title=f"test_title_{i}", content=f"test_content_{i}", user=test_user
        )

    endpoint = reverse("home:home_page")

    response_page1 = client.get(endpoint)
    assert response_page1.status_code == 200
    assert "articles" in response_page1.context
    assert len(response_page1.context["articles"]) == 10

    response_page2 = client.get(endpoint + "?page=2")
    assert response_page2.status_code == 200
    assert len(response_page2.context["articles"]) == 1


@pytest.mark.django_db
@pytest.mark.parametrize(
    "invalid_param",
    ["?page=abc", "?page=-1", "?page=999999"],
    ids=["non_numeric", "negative", "too_large"],
)
def test_home_view_invalid_get_params_does_not_crash(client, invalid_param):
    endpoint = reverse("home:home_page") + invalid_param
    response = client.get(endpoint)

    assert response.status_code != 500
    assert response.status_code in [200, 404]
