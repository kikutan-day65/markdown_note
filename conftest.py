import pytest
from django.contrib.auth import get_user_model


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
