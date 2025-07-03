import os
import re

from django.conf import settings
from django.core.files import File

from home.models import ArticleImage


# meida/にしたいのだが、これは開発用である。そのためどうにかしてsetingsからこれを取得する必要がある
def process_article_images(article, user_id):
    content = article.content
    print(content)
    article_images = re.findall(
        rf"article_images/{user_id}/tmp/[a-zA-Z0-9]+\.(?:jpg|jpeg|png|gif|webp|bmp|svg)",
        content,
    )

    if article_images:
        for image in article_images:
            filename = image.split(sep="/")[-1]
            temp_image_path = f"{settings.MEDIA_ROOT}/{image}"

            with open(temp_image_path, "+rb") as f:
                image_obj = File(f)
                image_instance = ArticleImage(article=article)
                image_instance.article_image.save(filename, image_obj)

            new_image_path = f"article_images/{user_id}/{article.id}/{filename}"

            content = content.replace(image, new_image_path)

            os.remove(temp_image_path)

        article.content = content

    return article
