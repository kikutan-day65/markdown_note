import os
from uuid import uuid4

from django.utils import timezone


def article_images_path(instance, filename):
    user_id = instance.user.id
    date = timezone.now().strftime("%Y%m%d")
    extension = filename.split(".")[-1]
    new_filename = f"{uuid4().hex}.{extension}"

    return f"article_images/{user_id}/{date}/{new_filename}"
