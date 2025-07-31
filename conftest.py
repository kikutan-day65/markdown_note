import pytest
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile

from home.models import Article

CustomUser = get_user_model()


@pytest.fixture
def user(db):
    """Create a user for the test"""
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
    user = CustomUser.objects.create_user(
        username="takenuser",
        password="testpassword123",
        email="takenuser@example.com",
        first_name="Test",
        last_name="User",
    )
    return user


@pytest.fixture
def another_user(db):
    """Create another user for test"""
    another_user = CustomUser.objects.create_user(
        username="anotheruser",
        password="testpassword123",
        email="another_user@example.com",
        first_name="Another",
        last_name="User",
    )
    return another_user


@pytest.fixture
def authenticated_client(client, user):
    client.login(username="testuser", password="testpassword123")
    return client


@pytest.fixture
def article(user) -> Article:
    """Creates Article instance for test

    Args:
        user: user for test

    Returns:
        Article: Article instance by user
    """
    article = Article.objects.create(
        title="test_title", markdown_content="test_content", user=user
    )

    return article


@pytest.fixture
def article_form_data() -> dict[str, str]:
    """Valid form data to create Article instance

    Returns:
        dict[str, str]: form data with title and markdown_content
    """
    form_data = {
        "title": "Test Title",
        "markdown_content": "## This is a test markdown",
    }
    return form_data


@pytest.fixture
def image():
    image = SimpleUploadedFile(
        name="test.jpg", content=b"dummy image data", content_type="image/jpeg"
    )
    return image
