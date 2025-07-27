import re

import markdown
import nh3
from bs4 import BeautifulSoup
from django.conf import settings

from home.constants import (
    MAX_FILES_PER_USER,
    MAX_IMAGE_SIZE,
    MAX_UNASSOCIATED_FILES_PER_USER,
)
from home.messages import (
    IMAGE_SIZE_ERROR,
    MAX_FILES_ERROR,
    MAX_UNASSOCIATED_FILES_ERROR,
)
from home.models import Article, ArticleImage


def convert_to_html(content: str) -> str:
    """Convert markdown content to sanitized html content

    Args:
        content (str): markdown content

    Returns:
        str: sanitized html content
    """
    raw_content = markdown.markdown(
        content,
        extensions=["extra", "codehilite", "toc", "admonition", "smarty"],
    )

    html_content = sanitize_content(raw_content)

    return html_content


def sanitize_content(content: str) -> str:
    """Sanitize raw html content

    Args:
        content (str): raw html content

    Returns:
        str: sanitized html content
    """
    return nh3.clean(
        content,
        tags=settings.NH3_HTML_SANITIZERS["tags"],
        attributes=settings.NH3_HTML_SANITIZERS["attributes"],
        url_schemes=settings.NH3_HTML_SANITIZERS["url_schemes"],
    )


def associate_images_with_article(content: str, article: Article) -> None:
    """Associate images in article with article id

    Args:
        content (str): html content
        article (Article): Article object
    """
    image_paths: list = extract_image_paths(content)

    if image_paths:
        ArticleImage.objects.filter(
            article_image__in=image_paths,
            article=None,
            user=article.user,
        ).update(article=article)


def extract_image_paths(content: str) -> list[str]:
    """Extract image url from img tag in html content

    Args:
        content (str): html content

    Returns:
        list[str]: list of extracted image url
    """
    image_paths = []
    pattern = (
        r"article_images/\d+/\d{8}/[a-f0-9\-]{32,36}\.(?:jpg|jpeg|png|gif|webp|bmp|svg)"
    )
    soup = BeautifulSoup(content, "html.parser")

    img_tags = soup.find_all("img")
    for img in img_tags:
        src = img.get("src")

        match = re.search(pattern, src)
        if match:
            image_paths.append(match.group())

    return image_paths


def delete_unused_images(content: str, article: Article) -> None:
    """Delete unused images in article from database

    Args:
        content (str): html content
        article (Article): Article object
    """
    # Delete unassociated images uploaded by the article's user
    ArticleImage.objects.filter(
        article=None,
        user=article.user,
    ).delete()

    # Delete images linked to this article but no longer used in content
    image_paths: list = extract_image_paths(content)

    ArticleImage.objects.filter(
        article=article,
        user=article.user,
    ).exclude(article_image__in=image_paths).delete()


def is_valid_upload(user, image_file):
    if image_file.size > MAX_IMAGE_SIZE:
        return False, IMAGE_SIZE_ERROR

    # Number of unassociated files uploaded by user
    unassociated_files = ArticleImage.objects.filter(article=None, user=user).count()
    if unassociated_files >= MAX_UNASSOCIATED_FILES_PER_USER:
        return False, MAX_UNASSOCIATED_FILES_ERROR

    # Number of files in total used by user
    total_files = ArticleImage.objects.filter(user=user).count()
    if total_files >= MAX_FILES_PER_USER:
        return False, MAX_FILES_ERROR

    return True, None
