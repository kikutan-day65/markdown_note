import pytest

from user.forms import UserUpdateForm


@pytest.mark.django_db
def test_user_update_form(user):
    form_data = {
        "username": "testuser_updated",
        "email": "testuser_updated@example.com",
        "first_name": "Test_updated",
        "last_name": "User_updated",
    }
    form = UserUpdateForm(instance=user, data=form_data)

    assert form.is_valid()


@pytest.mark.django_db
def test_user_update_form_with_existent_username(user, taken_user):
    form_data = {
        "username": "takenuser",
        "email": "testuser@example.com",
        "first_name": "Test",
        "last_name": "User",
    }
    form = UserUpdateForm(instance=user, data=form_data)

    assert not form.is_valid()


@pytest.mark.django_db
@pytest.mark.parametrize(
    "username, email, first_name, last_name",
    [
        (None, "testuser_updated@example.com", "Test_updated", "User_updated"),
        ("testuser_updated", None, "Test_updated", "User_updated"),
        ("testuser_updated", "testuser_updated@example.com", None, "User_updated"),
        ("testuser_updated", "testuser_updated@example.com", "Test_updated", None),
    ],
    ids=[
        "username",
        "email",
        "first_name",
        "last_name",
    ],
)
def test_user_update_form_without_required_fields(
    user, username, email, first_name, last_name
):
    form_data = {
        "username": username,
        "email": email,
        "first_name": first_name,
        "last_name": last_name,
    }
    form = UserUpdateForm(instance=user, data=form_data)

    assert not form.is_valid()
