import pytest
from django.contrib.auth import get_user_model
from django.db import IntegrityError

CustomUser = get_user_model()


@pytest.mark.django_db
def test_create_user():
    user = CustomUser.objects.create_user(
        username="testuser",
        password="testpassword123",
        email="testuser@example.com",
        first_name="Test",
        last_name="User",
    )

    assert user.id is not None
    assert user.username == "testuser"
    assert user.check_password("testpassword123")
    assert user.email == "testuser@example.com"
    assert user.first_name == "Test"
    assert user.last_name == "User"


@pytest.mark.django_db
@pytest.mark.parametrize(
    "first_name, last_name",
    [
        (None, "User"),
        ("Test", None),
    ],
    ids=[
        "first_name",
        "last_name",
    ],
)
def test_create_user_without_required_fields(first_name, last_name):
    with pytest.raises(IntegrityError):
        CustomUser.objects.create_user(
            username="testuser",
            password="testpassword123",
            email="testuser@examle.com",
            first_name=first_name,
            last_name=last_name,
        )
