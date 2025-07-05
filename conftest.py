import pytest
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile

from home.models import Article


@pytest.fixture
def test_user(db):
    """Create a user for the test"""
    CustomUser = get_user_model()
    user = CustomUser.objects.create_user(
        username="testuser",
        password="testpassword123",
        email="testuser@example.com",
        first_name="Test",
        last_name="User",
    )
    return user


@pytest.fixture
def taken_user(db):
    """Create a user for the test"""
    CustomUser = get_user_model()
    user = CustomUser.objects.create_user(
        username="takenuser",
        password="testpassword123",
        email="takenuser@example.com",
        first_name="Test",
        last_name="User",
    )
    return user


@pytest.fixture
def authenticated_client(client, test_user):
    client.login(username="testuser", password="testpassword123")
    return client


@pytest.fixture
def test_article(test_user):
    article = Article.objects.create(
        title="test_title", content="test_content", user=test_user
    )

    return article


@pytest.fixture
def test_image():
    test_image = SimpleUploadedFile(
        name="test_image.jpg", content=b"test-image", content_type="image/jpeg"
    )
    return test_image
