from django.contrib import messages
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse, reverse_lazy

from home.messages import (
    ARTICLE_CREATE_SUCCESS,
    ARTICLE_DELETE_SUCCESS,
    ARTICLE_UPDATE_SUCCESS,
)
from home.models import Article
from home.views import (
    ArticleCreateView,
    ArticleDeleteView,
    ArticleDetailView,
    ArticleUpdateView,
    HomeView,
)
from user.models import CustomUser


class HomeViewTest(TestCase):
    def test_get_status_code_200(self):
        response = self.client.get(reverse_lazy("home:home_page"))
        self.assertEqual(response.status_code, 200)

    def test_template_used(self):
        response = self.client.get(reverse_lazy("home:home_page"))
        self.assertTemplateUsed(response, HomeView.template_name)

    def test_articles_in_context(self):
        response = self.client.get(reverse_lazy("home:home_page"))
        self.assertIn(HomeView.context_object_name, response.context)

    def test_pagination(self):
        user = CustomUser.objects.create_user(
            username="testuser",
            password="passwdfortest123",
            email="testuser@gmail.com",
            first_name="Test",
            last_name="User",
        )
        for i in range(10):
            article = Article(title=f"title{i}", content=f"content{i}", user=user)
            article.save()
        response = self.client.get(reverse_lazy("home:home_page"))
        self.assertEqual(len(response.context["articles"]), 10)

    def test_filter_class(self):
        response = self.client.get(reverse_lazy("home:home_page"))
        self.assertIsInstance(response.context["filter"], HomeView.filterset_class)


class ArticleCreateViewTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="testuser",
            password="passwdfortest123",
            email="testuser@gmail.com",
            first_name="Test",
            last_name="User",
        )
        self.client.login(username="testuser", password="passwdfortest123")

    def test_get_status_code_200(self):
        response = self.client.get(reverse_lazy("home:article_create"))
        self.assertEqual(response.status_code, 200)

    def test_template_used(self):
        response = self.client.get(reverse_lazy("home:article_create"))
        self.assertTemplateUsed(response, ArticleCreateView.template_name)

    def test_article_create_form_in_context(self):
        response = self.client.get(reverse_lazy("home:article_create"))
        self.assertIn("article_create_form", response.context)

    def test_redirect_to_success_url(self):
        data = {
            "title": "test_title",
            "content": "test_content",
        }
        response = self.client.post(reverse("home:article_create"), data)
        self.assertEqual(response.url, reverse_lazy("home:home_page"))

    def test_article_user_is_request_user(self):
        data = {
            "title": "test_title",
            "content": "test_content",
        }
        self.client.post(reverse("home:article_create"), data)
        article = Article.objects.latest("id")
        self.assertEqual(article.user, self.user)

    def test_not_logged_in_user(self):
        self.client.post(reverse_lazy("user:logout"))
        response = self.client.get(reverse_lazy("home:article_create"))
        self.assertEqual(
            response.url,
            f"{reverse_lazy('user:login')}?next={reverse_lazy('home:article_create')}",
        )

    def test_success_messages(self):
        data = {
            "title": "test_title",
            "content": "test_content",
        }
        response = self.client.post(reverse("home:article_create"), data)
        message_list = list(get_messages(response.wsgi_request))
        self.assertIn(ARTICLE_CREATE_SUCCESS, [msg.message for msg in message_list])

    def test_error_messages(self):
        data = {
            "title": "",
            "content": "test_content",
        }
        response = self.client.post(reverse("home:article_create"), data)
        message_list = list(get_messages(response.wsgi_request))
        self.assertTrue(any(msg.level == messages.ERROR for msg in message_list))


class ArticleDetailViewTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="testuser",
            password="passwdfortest123",
            email="testuser@gmail.com",
            first_name="Test",
            last_name="User",
        )

        self.article = Article(
            title="test_title", content="test_content", user=self.user
        )
        self.article.save()

    def test_get_status_code_200(self):
        response = self.client.get(
            reverse("home:article_detail", kwargs={"pk": self.article.pk})
        )
        self.assertEqual(response.status_code, 200)

    def test_template_used(self):
        response = self.client.get(
            reverse("home:article_detail", kwargs={"pk": self.article.pk})
        )
        self.assertTemplateUsed(response, ArticleDetailView.template_name)

    def test_article_detail_in_context(self):
        response = self.client.get(
            reverse("home:article_detail", kwargs={"pk": self.article.pk})
        )
        self.assertIn(ArticleDetailView.context_object_name, response.context)

    def test_article_not_exist(self):
        response = self.client.get(reverse("home:article_detail", kwargs={"pk": 2}))
        self.assertEqual(response.status_code, 404)


class ArticleUpdateViewTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="testuser",
            password="passwdfortest123",
            email="testuser@gmail.com",
            first_name="Test",
            last_name="User",
        )
        self.client.login(username="testuser", password="passwdfortest123")

        self.article = Article(
            title="test_title", content="test_content", user=self.user
        )
        self.article.save()

    def test_get_status_code_200(self):
        response = self.client.get(
            reverse("home:article_update", kwargs={"pk": self.article.pk})
        )
        self.assertEqual(response.status_code, 200)

    def test_template_used(self):
        response = self.client.get(
            reverse("home:article_update", kwargs={"pk": self.article.pk})
        )
        self.assertTemplateUsed(response, ArticleUpdateView.template_name)

    def test_not_logged_in_user(self):
        self.client.post(reverse_lazy("user:logout"))
        response = self.client.get(
            reverse("home:article_update", kwargs={"pk": self.article.pk})
        )
        self.assertEqual(
            response.url,
            f"{reverse_lazy('user:login')}?next={reverse('home:article_update', kwargs={'pk': self.article.pk})}",
        )

    def test_article_update_form_in_context(self):
        response = self.client.get(
            reverse("home:article_update", kwargs={"pk": self.article.pk})
        )
        self.assertIn("article_update_form", response.context)

    def test_redirect_to_success_url(self):
        data = {
            "title": "test_title_updated",
            "content": "test_content",
        }
        response = self.client.post(
            reverse("home:article_update", kwargs={"pk": self.article.pk}), data
        )
        self.assertEqual(
            response.url, reverse("home:article_detail", kwargs={"pk": self.article.pk})
        )

    def test_modified_at(self):
        self.assertIsNone(self.article.modified_at)
        data = {
            "title": "test_title_updated",
            "content": "test_content",
        }
        self.client.post(
            reverse("home:article_update", kwargs={"pk": self.article.pk}), data
        )
        self.article.refresh_from_db()
        self.assertIsNotNone(self.article.modified_at)

    def test_article_in_context(self):
        response = self.client.get(
            reverse("home:article_update", kwargs={"pk": self.article.pk})
        )
        self.assertIn(ArticleUpdateView.context_object_name, response.context)

    def test_other_user_update_error(self):
        CustomUser.objects.create_user(
            username="other_user",
            password="passwdfortest123",
            email="other_user@gmail.com",
            first_name="Test",
            last_name="User",
        )
        self.client.login(username="other_user", password="passwdfortest123")

        data = {
            "title": "test_title_updated",
            "content": "test_content",
        }
        response = self.client.post(
            reverse("home:article_update", kwargs={"pk": self.article.pk}), data
        )
        self.assertEqual(response.status_code, 404)

    def test_success_messages(self):
        data = {
            "title": "test_title_updated",
            "content": "test_content",
        }
        response = self.client.post(
            reverse("home:article_update", kwargs={"pk": self.article.pk}), data
        )
        message_list = list(get_messages(response.wsgi_request))
        self.assertIn(ARTICLE_UPDATE_SUCCESS, [msg.message for msg in message_list])

    def test_error_messages(self):
        data = {
            "title": "",
            "content": "test_content",
        }
        response = self.client.post(
            reverse("home:article_update", kwargs={"pk": self.article.pk}), data
        )
        message_list = list(get_messages(response.wsgi_request))
        self.assertTrue(any(msg.level == messages.ERROR for msg in message_list))


class ArticleDeleteViewTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="testuser",
            password="passwdfortest123",
            email="testuser@gmail.com",
            first_name="Test",
            last_name="User",
        )
        self.client.login(username="testuser", password="passwdfortest123")

        self.article = Article(
            title="test_title", content="test_content", user=self.user
        )
        self.article.save()

    def test_get_status_code_200(self):
        response = self.client.get(
            reverse("home:article_delete", kwargs={"pk": self.article.pk})
        )
        self.assertEqual(response.status_code, 200)

    def test_template_used(self):
        response = self.client.get(
            reverse("home:article_delete", kwargs={"pk": self.article.pk})
        )
        self.assertTemplateUsed(response, ArticleDeleteView.template_name)

    def test_article_in_context(self):
        response = self.client.get(
            reverse("home:article_delete", kwargs={"pk": self.article.pk})
        )
        self.assertIn(ArticleDeleteView.context_object_name, response.context)

    def test_not_logged_in_user(self):
        self.client.post(reverse_lazy("user:logout"))
        response = self.client.get(
            reverse("home:article_delete", kwargs={"pk": self.article.pk})
        )
        self.assertEqual(
            response.url,
            f"{reverse_lazy('user:login')}?next={reverse('home:article_delete', kwargs={'pk': self.article.pk})}",
        )

    def test_other_user_update_error(self):
        CustomUser.objects.create_user(
            username="other_user",
            password="passwdfortest123",
            email="other_user@gmail.com",
            first_name="Test",
            last_name="User",
        )
        self.client.login(username="other_user", password="passwdfortest123")

        response = self.client.post(
            reverse("home:article_delete", kwargs={"pk": self.article.pk})
        )
        self.assertEqual(response.status_code, 404)

    def test_redirect_to_success_url(self):
        response = self.client.post(
            reverse("home:article_delete", kwargs={"pk": self.article.pk})
        )
        self.assertEqual(response.url, reverse_lazy("home:home_page"))

    def test_success_messages(self):
        response = self.client.post(
            reverse("home:article_delete", kwargs={"pk": self.article.pk})
        )
        message_list = list(get_messages(response.wsgi_request))
        self.assertIn(ARTICLE_DELETE_SUCCESS, [msg.message for msg in message_list])
