from django.urls import path

from .views import (
    ArticleCreateView,
    ArticleDeleteView,
    ArticleDetailView,
    ArticleUpdateView,
    HomeView,
    upload_article_images,
)

# fmt: off
app_name = "home"
urlpatterns = [
    path("", HomeView.as_view(), name="home_page"),
    path("article/<int:pk>/", ArticleDetailView.as_view(), name="article_detail"),
    path("article/create/", ArticleCreateView.as_view(), name="article_create"),
    path("article/update/<int:pk>/", ArticleUpdateView.as_view(), name="article_update"),
    path("article/delete/<int:pk>/", ArticleDeleteView.as_view(), name="article_delete"),
    path("upload-article-images/", upload_article_images, name="upload_article_images"),
]
# fmt: on
