from django.conf import settings
from django.db import models
from home.utils.filepath import article_images_path


class Article(models.Model):
    title = models.CharField(max_length=255, null=False, blank=False)
    content = models.TextField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="articles"
    )

    def __str__(self):
        return self.title


class ArticleImage(models.Model):
    article_image = models.ImageField(upload_to=article_images_path)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name="images"
    )
