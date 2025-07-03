import pytest

from user.forms import UserRegisterForm


@pytest.mark.django_db
def test_user_register_form():
    form_data = {
        "username": "testuser",
        "email": "testuser@example.com",
        "password1": "testpassword123",
        "password2": "testpassword123",
        "first_name": "Test",
        "last_name": "User",
    }
    form = UserRegisterForm(data=form_data)

    assert form.is_valid()


# fmt: off
@pytest.mark.django_db
@pytest.mark.parametrize(
    "username, email, first_name, last_name, password1, password2",
    [
        (None, "testuser@example.com", "Test","User", "testpassword123", "testpassword123"),
        ("testuser", None, "Test", "User", "testpassword123", "testpassword123"),
        ("testuser", "testuser@example.com", None, "User", "testpassword123", "testpassword123"),
        ("testuser", "testuser@example.com", "Test", None, "testpassword123", "testpassword123"),
        ("testuser", "testuser@example.com", "Test", "User", None, "testpassword123"),
        ("testuser", "testuser@example.com", "Test", "User", "testpassword123", None),
    ],
    ids=[
        "username",
        "email",
        "first_name",
        "last_name",
        "password1",
        "password2",
    ],
)
def test_user_register_form_without_required_fields(
    username, email, first_name, last_name, password1, password2
):
    form_data = {
        "username": username,
        "email": email,
        "password1": password1,
        "password2": password2,
        "first_name": first_name,
        "last_name": last_name,
    }
    form = UserRegisterForm(data=form_data)

    assert not form.is_valid()
# fmt: on


@pytest.mark.django_db
def test_user_register_form_with_blank_password():
    form_data = {
        "username": "testuser",
        "email": "testuser@example.com",
        "password1": " ",
        "password2": " ",
        "first_name": "Test",
        "last_name": "User",
    }
    form = UserRegisterForm(data=form_data)

    assert not form.is_valid()
    assert "password1" in form.errors


@pytest.mark.django_db
def test_user_register_form_with_password_mismatch():
    form_data = {
        "username": "testuser",
        "email": "testuser@example.com",
        "password1": "testuser123",
        "password2": "testuser12345",
        "first_name": "Test",
        "last_name": "User",
    }
    form = UserRegisterForm(data=form_data)

    assert not form.is_valid()
    assert "password2" in form.errors


@pytest.mark.django_db
def test_user_register_form_with_username(test_user):
    form_data = {
        "username": "testuser",
        "email": "newuser@example.com",
        "password1": "testpassword123",
        "password2": "testpassword123",
        "first_name": "Test",
        "last_name": "User",
    }

    form = UserRegisterForm(data=form_data)

    assert not form.is_valid()
    assert "username" in form.errors
