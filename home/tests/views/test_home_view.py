import pytest
from django.urls import reverse

from home.filters import ArticleFilter
from home.models import Article


@pytest.mark.django_db
def test_renders_template(client):
    endpoint = reverse("home:home_page")
    response = client.get(endpoint)
    template_names = [
        template.name for template in response.templates if template.name is not None
    ]

    assert response.status_code == 200
    assert "home/home.html" in template_names


@pytest.mark.django_db
def test_includes_articles_in_context(client):
    endpoint = reverse("home:home_page")
    response = client.get(endpoint)

    assert response.status_code == 200
    assert "articles" in response.context


@pytest.mark.django_db
def test_articles_descending_ordered_by_created_at(client, user):
    article_1 = Article.objects.create(
        title="Article 1", markdown_content="Article content 1", user=user
    )
    article_2 = Article.objects.create(
        title="Article 2", markdown_content="Article content 2", user=user
    )
    endpoint = reverse("home:home_page")
    response = client.get(endpoint)
    article_list = list(response.context["articles"])

    assert response.status_code == 200
    assert article_2.created_at > article_1.created_at
    assert article_list[0] == article_2
    assert article_list[-1] == article_1


@pytest.mark.django_db
def test_10_articles_per_page(client, user):
    for i in range(15):
        Article.objects.create(
            title=f"Article {i}", markdown_content=f"Article content {i}", user=user
        )
    endpoint = reverse("home:home_page")
    response_page_1 = client.get(endpoint)
    articles_page_1 = response_page_1.context["articles"]

    response_page_2 = client.get(endpoint + "?page=2")
    articles_page_2 = response_page_2.context["articles"]

    assert response_page_1.status_code == 200
    assert len(articles_page_1) == 10

    assert response_page_2.status_code == 200
    assert len(articles_page_2) == 5


@pytest.mark.django_db
def test_article_filter_in_context(client):
    endpoint = reverse("home:home_page")
    response = client.get(endpoint)

    assert response.status_code == 200
    assert isinstance(response.context["filter"], ArticleFilter)


@pytest.mark.django_db
def test_page_is_out_of_range(client):
    dummy_page = 999
    endpoint = reverse("home:home_page")
    response = client.get(endpoint + f"?page={dummy_page}")

    assert response.status_code == 404
