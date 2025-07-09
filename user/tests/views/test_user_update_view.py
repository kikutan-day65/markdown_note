import pytest
from django.contrib.messages import get_messages
from django.urls import reverse

from user.messages import USER_UPDATE_SUCCESS


@pytest.mark.django_db
def test_user_update_view_get(authenticated_client, test_user):
    endpoint = reverse("user:update", kwargs={"pk": test_user.pk})
    response = authenticated_client.get(endpoint)

    assert response.status_code == 200


@pytest.mark.django_db
def test_user_update_view_context(authenticated_client, test_user):
    endpoint = reverse("user:update", kwargs={"pk": test_user.pk})
    response = authenticated_client.get(endpoint)

    assert "user_update_form" in response.context


@pytest.mark.django_db
def test_user_update_view(authenticated_client, test_user):
    form_data = {
        "username": "testuser_updated",
        "email": "testuser_updated@example.com",
        "first_name": "Test_updated",
        "last_name": "User_updated",
    }
    endpoint = reverse("user:update", kwargs={"pk": test_user.pk})
    response = authenticated_client.post(endpoint, data=form_data)

    assert response.status_code == 302

    test_user.refresh_from_db()
    assert test_user.username == "testuser_updated"
    assert test_user.email == "testuser_updated@example.com"
    assert test_user.first_name == "Test_updated"
    assert test_user.last_name == "User_updated"


@pytest.mark.django_db
def test_user_update_view_success_message(authenticated_client, test_user):
    form_data = {
        "username": "testuser_updated",
        "email": "testuser_updated@example.com",
        "first_name": "Test_updated",
        "last_name": "User_updated",
    }
    endpoint = reverse("user:update", kwargs={"pk": test_user.pk})
    response = authenticated_client.post(endpoint, data=form_data)
    messages = list(get_messages(response.wsgi_request))

    assert response.status_code == 302
    assert any(USER_UPDATE_SUCCESS in str(m) for m in messages)


@pytest.mark.django_db
def test_user_update_view_get_unauthorized_user(client, test_user):
    endpoint = reverse("user:update", kwargs={"pk": test_user.pk})
    login_url = reverse("user:login")
    response = client.get(endpoint)

    assert response.status_code == 302
    assert response.url == f"{login_url}?next={endpoint}"


@pytest.mark.django_db
def test_user_update_view_post_unauthorized_user(client, test_user):
    form_data = {
        "username": "testuser_updated",
        "email": "testuser_updated@example.com",
        "first_name": "Test_updated",
        "last_name": "User_updated",
    }
    endpoint = reverse("user:update", kwargs={"pk": test_user.pk})
    login_url = reverse("user:login")
    response = client.post(endpoint, data=form_data)

    assert response.status_code == 302
    assert response.url == f"{login_url}?next={endpoint}"


@pytest.mark.django_db
def test_user_update_view_get_other_user(authenticated_client, taken_user):
    endpoint = reverse("user:update", kwargs={"pk": taken_user.pk})
    response = authenticated_client.get(endpoint)

    assert response.status_code == 404


@pytest.mark.django_db
def test_user_update_view_post_other_user(authenticated_client, taken_user):
    form_data = {
        "username": "taken_user_updated",
        "email": "taken_user_updated@example.com",
        "first_name": "taken_Test_updated",
        "last_name": "taken_User_updated",
    }
    endpoint = reverse("user:update", kwargs={"pk": taken_user.pk})
    response = authenticated_client.post(endpoint, data=form_data)

    assert response.status_code == 404

    taken_user.refresh_from_db()
    assert taken_user.username != "taken_user_updated"
    assert taken_user.email != "taken_user_updated@example.com"


@pytest.mark.django_db
def test_user_update_view_taken_username(authenticated_client, test_user, taken_user):
    form_data = {
        "username": "takenuser",
        "email": "testuser_updated@example.com",
        "first_name": "Test_updated",
        "last_name": "User_updated",
    }
    endpoint = reverse("user:update", kwargs={"pk": test_user.pk})
    response = authenticated_client.post(endpoint, data=form_data)
    form = response.context["user_update_form"]

    assert response.status_code == 200
    assert not form.is_valid()
    assert "username" in form.errors


@pytest.mark.django_db
def test_user_update_view_taken_email(authenticated_client, test_user, taken_user):
    form_data = {
        "username": "testuser",
        "email": "takenuser@example.com",
        "first_name": "Test_updated",
        "last_name": "User_updated",
    }
    endpoint = reverse("user:update", kwargs={"pk": test_user.pk})
    response = authenticated_client.post(endpoint, data=form_data)
    form = response.context["user_update_form"]

    assert response.status_code == 200
    assert not form.is_valid()
    assert "email" in form.errors


@pytest.mark.django_db
@pytest.mark.parametrize(
    "missing_field, form_data",
    [
        (
            "username",
            {
                "username": "",
                "email": "testuser_updated@example.com",
                "first_name": "Test_updated",
                "last_name": "User_updated",
            },
        ),
        (
            "email",
            {
                "username": "testuser_updated",
                "email": "",
                "first_name": "Test_updated",
                "last_name": "User_updated",
            },
        ),
        (
            "first_name",
            {
                "username": "testuser_updated",
                "email": "testuser_updated@example.com",
                "first_name": "",
                "last_name": "User_updated",
            },
        ),
        (
            "last_name",
            {
                "username": "testuser_updated",
                "email": "testuser_updated@example.com",
                "first_name": "Test_updated",
                "last_name": "",
            },
        ),
    ],
    ids=["username", "email", "first_name", "last_name"],
)
def test_user_update_view_without_required_fields(
    authenticated_client, test_user, missing_field, form_data
):
    endpoint = reverse("user:update", kwargs={"pk": test_user.pk})
    response = authenticated_client.post(endpoint, data=form_data)
    form = response.context["user_update_form"]

    assert response.status_code == 200
    assert not form.is_valid()
    assert missing_field in form.errors
