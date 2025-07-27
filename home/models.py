from django.conf import settings
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver

from home.utils.filepath import article_images_path


class Article(models.Model):
    title = models.CharField(max_length=255, null=False, blank=False)
    markdown_content = models.TextField(null=False, blank=False)
    html_content = models.TextField(null=False, blank=False)
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
        Article,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="images",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="uploaded_article_images",
    )


@receiver(post_delete, sender=ArticleImage)
def delete_article_image_file(sender, instance, **kwargs):
    if instance.article_image:
        instance.article_image.delete(save=False)
