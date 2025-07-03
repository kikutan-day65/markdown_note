import pytest

from user.forms import UserLoginForm


@pytest.mark.django_db
def test_user_login_form_with_username(test_user):
    form_data = {
        "username": "testuser",
        "password": "testpassword123",
    }
    form = UserLoginForm(request=None, data=form_data)

    assert form.is_valid()


@pytest.mark.django_db
def test_user_login_form_with_email(test_user):
    form_data = {
        "username": "testuser@example.com",
        "password": "testpassword123",
    }
    form = UserLoginForm(request=None, data=form_data)

    assert form.is_valid()


@pytest.mark.django_db
@pytest.mark.parametrize(
    "username, password",
    [
        ("nonexistent_user", "testpassword123"),
        ("testuser", "wrong_password_for_username"),
    ],
    ids=[
        "nonexistent_username",
        "wrong_password",
    ],
)
def test_user_login_form_error_username(test_user, username, password):
    form_data = {
        "username": username,
        "password": password,
    }
    form = UserLoginForm(request=None, data=form_data)

    assert not form.is_valid()


@pytest.mark.django_db
@pytest.mark.parametrize(
    "email, password",
    [
        ("nonexistent_email@example.com", "testpassword123"),
        ("testuser@example.com", "wrong_password"),
    ],
    ids=[
        "nonexistent_email",
        "wrong_password_for_email",
    ],
)
def test_user_login_form_error_email(test_user, email, password):
    form_data = {
        "username": email,
        "password": password,
    }
    form = UserLoginForm(request=None, data=form_data)

    assert not form.is_valid()


@pytest.mark.django_db
@pytest.mark.parametrize(
    "username, password",
    [
        ("", "testuser123"),
        ("testuser", ""),
    ],
    ids=["username", "password"],
)
def test_user_login_form_without_required_fields(test_user, username, password):
    form_data = {
        "username": username,
        "password": password,
    }
    form = UserLoginForm(request=None, data=form_data)

    assert not form.is_valid()
