import pytest
from django.db import IntegrityError
from django.utils import timezone

from home.models import Article


@pytest.mark.django_db
def test_create_article(user):
    article = Article.objects.create(
        title="test_title",
        markdown_content="test_content",
        html_content="<p>test_content</p>",
        user=user,
    )

    assert article.title == "test_title"
    assert article.markdown_content == "test_content"
    assert article.html_content == "<p>test_content</p>"
    assert article.user == user


@pytest.mark.django_db
def test_created_at_is_set_automatically(user):
    before = timezone.now()
    article = Article.objects.create(
        title="test_title",
        markdown_content="test_content",
        html_content="<p>test_content</p>",
        user=user,
    )
    after = timezone.now()

    assert article.created_at
    assert before < article.created_at < after


@pytest.mark.django_db
def test_modified_at_is_null(user):
    article = Article.objects.create(
        title="test_title",
        markdown_content="test_content",
        html_content="<p>test_content</p>",
        user=user,
    )

    assert article.modified_at is None


@pytest.mark.django_db
def test_modified_at_is_null(user):
    article = Article.objects.create(
        title="test_title",
        markdown_content="test_content",
        html_content="<p>test_content</p>",
        user=user,
    )

    assert str(article) == article.title


@pytest.mark.django_db
def user_can_access_related_articles(user):
    Article.objects.create(
        title="test_title_1",
        markdown_content="test_content_1",
        html_content="<p>test_content_1</p>",
        user=user,
    )
    Article.objects.create(
        title="test_title_2",
        markdown_content="test_content_2",
        html_content="<p>test_content_2</p>",
        user=user,
    )

    articles = user.articles.all()
    titles = [article.title for article in articles]

    assert articles.count() == 2
    assert "test_title_1" in titles
    assert "test_title_2" in titles


@pytest.mark.django_db
@pytest.mark.parametrize(
    "title, markdown_content, html_content, user_fk",
    [
        (None, "test_content", "<p>test_content</p>", True),
        ("test_title", None, None, True),
        ("test_title", "test_content", "<p>test_content</p>", False),
    ],
    ids=["missing_title", "missing_content", "missing_user"],
)
def test_create_article_without_required_fields(
    user, title, markdown_content, html_content, user_fk
):
    user = user if user_fk else None

    with pytest.raises((ValueError, IntegrityError)):
        Article.objects.create(
            title=title,
            markdown_content=markdown_content,
            html_content=html_content,
            user=user,
        )
