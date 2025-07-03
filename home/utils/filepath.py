import os
from uuid import uuid4


def article_images_path(instance, filename):
    article_id = instance.article.id
    user_id = instance.article.user.id

    return f"article_images/{user_id}/{article_id}/{filename}"


def temp_article_images_path(user, filename):
    ext = os.path.splitext(filename)[1]
    new_filename = f"{uuid4().hex}{ext}"
    user_id = user.id

    return f"article_images/{user_id}/tmp/{new_filename}"
