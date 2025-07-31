from uuid import UUID

import pytest
from django.utils import timezone

from home.utils.filepath import article_images_path


class DummyUser:
    def __init__(self, user_id):
        self.id = user_id


class DummyInstance:
    def __init__(self, user):
        self.user = user


@pytest.mark.parametrize("filename", ["example.jpg", "image.png", "test.jpeg"])
def test_article_images_path_returns_valid_format(filename):
    # Create dummy user and instance
    user_id = 1
    dummy_user = DummyUser(user_id=user_id)
    instance = DummyInstance(user=dummy_user)

    path = article_images_path(instance, filename)

    today = timezone.now().strftime("%Y%m%d")

    assert path.startswith(f"article_images/{user_id}/{today}/")
    assert path.endswith(f".{filename.split('.')[-1]}")

    # Check if path has a uuid part
    uuid_part = path.split("/")[-1].split(".")[0]
    UUID(uuid_part)
