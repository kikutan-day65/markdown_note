import pytest

from user.forms import UserPasswordChangeForm


@pytest.mark.django_db
def test_user_password_change_form(test_user):
    form_data = {
        "old_password": "testpassword123",
        "new_password1": "new_testpassword123",
        "new_password2": "new_testpassword123",
    }
    form = UserPasswordChangeForm(user=test_user, data=form_data)

    assert form.is_valid()


@pytest.mark.django_db
@pytest.mark.parametrize(
    "old_password, new_password1, new_password2",
    [
        (None, "new_testpassword123", "new_testpassword123"),
        ("testpassword123", None, "new_testpassword123"),
        ("testpassword123", "new_testpassword123", None),
    ],
    ids=["old_password", "new_password1", "new_password2"],
)
def test_user_password_change_form_without_required_fields(
    test_user, old_password, new_password1, new_password2
):
    form_data = {
        "old_password": old_password,
        "new_password1": new_password1,
        "new_password2": new_password2,
    }
    form = UserPasswordChangeForm(user=test_user, data=form_data)

    assert not form.is_valid()


@pytest.mark.django_db
def test_user_password_change_form_with_same_as_old_one(test_user):
    form_data = {
        "old_password": "testpassword123",
        "new_password1": "testpassword123",
        "new_password2": "testpassword123",
    }
    form = UserPasswordChangeForm(user=test_user, data=form_data)

    assert not form.is_valid()


@pytest.mark.django_db
def test_user_password_change_form_with_wrong_old_password(test_user):
    form_data = {
        "old_password": "wrong_old_password",
        "new_password1": "new_testpassword123",
        "new_password2": "new_testpassword123",
    }
    form = UserPasswordChangeForm(user=test_user, data=form_data)

    assert not form.is_valid()


@pytest.mark.django_db
def test_user_password_change_form_with_mismatch_password(test_user):
    form_data = {
        "old_password": "testpassword123",
        "new_password1": "new_testpassword123",
        "new_password2": "mismatch_testpassword123",
    }
    form = UserPasswordChangeForm(user=test_user, data=form_data)

    assert not form.is_valid()


@pytest.mark.django_db
@pytest.mark.parametrize(
    "old_password, new_password1, new_password2",
    [
        ("testpassword123", "testuser123", "testuser123"),
        ("testpassword123", "123", "123"),
    ],
    ids=["similar_to_username", "violates_password_security"],
)
def test_user_password_change_form_with_weak_one(
    test_user, old_password, new_password1, new_password2
):
    form_data = {
        "old_password": old_password,
        "new_password1": new_password1,
        "new_password2": new_password2,
    }
    form = UserPasswordChangeForm(user=test_user, data=form_data)

    assert not form.is_valid()
