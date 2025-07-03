from django.core.exceptions import ValidationError
from django.test import TestCase

from home.models import Article
from user.models import CustomUser


class ArticleModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="testuser",
            email="testuser@gmail.com",
            password="passwdfortest123",
            first_name="Test",
            last_name="User",
        )

    def test_article_create_success(self):
        article = Article(
            title="test title",
            content="test content",
            user=self.user,
        )
        article.full_clean()
        article.save()

        self.assertEqual(article.title, "test title")
        self.assertEqual(article.content, "test content")
        self.assertEqual(article.user, self.user)

    def test_article_without_title_error(self):
        with self.assertRaises(ValidationError):
            article = Article(
                title="",
                content="test content",
                user=self.user,
            )
            article.full_clean()

    def test_article_without_content_error(self):
        with self.assertRaises(ValidationError):
            article = Article(
                title="test title",
                content="",
                user=self.user,
            )
            article.full_clean()

    def test_article_without_user_error(self):
        with self.assertRaises(ValueError):
            article = Article(
                title="test title",
                content="test content",
                user="",
            )
