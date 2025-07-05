import pytest
from django.db import IntegrityError
from django.utils import timezone

from home.models import Article


@pytest.mark.django_db
def test_create_article(test_user):
    article = Article.objects.create(
        title="test_title", content="test_content", user=test_user
    )

    assert article.title == "test_title"
    assert article.content == "test_content"
    assert article.user == test_user


@pytest.mark.django_db
def test_created_at_is_set_automatically(test_user):
    before = timezone.now()
    article = Article.objects.create(
        title="test_title", content="test_content", user=test_user
    )
    after = timezone.now()

    assert article.created_at
    assert before < article.created_at < after


@pytest.mark.django_db
def test_modified_at_is_null(test_user):
    article = Article.objects.create(
        title="test_title", content="test_content", user=test_user
    )

    assert article.modified_at is None


@pytest.mark.django_db
def test_modified_at_is_null(test_user):
    article = Article.objects.create(
        title="test_title", content="test_content", user=test_user
    )

    assert str(article) == article.title


@pytest.mark.django_db
def test_user_can_access_related_articles(test_user):
    Article.objects.create(
        title="test_title_1", content="test_content_1", user=test_user
    )
    Article.objects.create(
        title="test_title_2", content="test_content_2", user=test_user
    )

    articles = test_user.articles.all()
    titles = [article.title for article in articles]

    assert articles.count() == 2
    assert "test_title_1" in titles
    assert "test_title_2" in titles


@pytest.mark.django_db
@pytest.mark.parametrize(
    "title, content, user_fk",
    [
        (None, "test_content", True),
        ("test_title", None, True),
        ("test_title", "test_content", False),
    ],
    ids=["missing_title", "missing_content", "missing_user"],
)
def test_create_article_without_required_fields(test_user, title, content, user_fk):
    user = test_user if user_fk else None

    with pytest.raises((ValueError, IntegrityError)):
        Article.objects.create(title=title, content=content, user=user)
