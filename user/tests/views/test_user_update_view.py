import pytest
from django.contrib.messages import get_messages
from django.urls import reverse

from user.messages import USER_UPDATE_SUCCESS


@pytest.mark.django_db
def test_user_update_view_get(authenticated_client, user):
    endpoint = reverse("user:update", kwargs={"pk": user.pk})
    response = authenticated_client.get(endpoint)

    assert response.status_code == 200


@pytest.mark.django_db
def test_user_update_view_context(authenticated_client, user):
    endpoint = reverse("user:update", kwargs={"pk": user.pk})
    response = authenticated_client.get(endpoint)

    assert "user_update_form" in response.context


@pytest.mark.django_db
def test_user_update_view(authenticated_client, user):
    form_data = {
        "username": "testuser_updated",
        "email": "testuser_updated@example.com",
        "first_name": "Test_updated",
        "last_name": "User_updated",
    }
    endpoint = reverse("user:update", kwargs={"pk": user.pk})
    response = authenticated_client.post(endpoint, data=form_data)

    assert response.status_code == 302

    user.refresh_from_db()
    assert user.username == "testuser_updated"
    assert user.email == "testuser_updated@example.com"
    assert user.first_name == "Test_updated"
    assert user.last_name == "User_updated"


@pytest.mark.django_db
def test_user_update_view_success_message(authenticated_client, user):
    form_data = {
        "username": "testuser_updated",
        "email": "testuser_updated@example.com",
        "first_name": "Test_updated",
        "last_name": "User_updated",
    }
    endpoint = reverse("user:update", kwargs={"pk": user.pk})
    response = authenticated_client.post(endpoint, data=form_data)
    messages = list(get_messages(response.wsgi_request))

    assert response.status_code == 302
    assert any(USER_UPDATE_SUCCESS in str(m) for m in messages)


@pytest.mark.django_db
def test_user_update_view_get_unauthorized_user(client, user):
    endpoint = reverse("user:update", kwargs={"pk": user.pk})
    login_url = reverse("user:login")
    response = client.get(endpoint)

    assert response.status_code == 302
    assert response.url == f"{login_url}?next={endpoint}"


@pytest.mark.django_db
def test_user_update_view_post_unauthorized_user(client, user):
    form_data = {
        "username": "testuser_updated",
        "email": "testuser_updated@example.com",
        "first_name": "Test_updated",
        "last_name": "User_updated",
    }
    endpoint = reverse("user:update", kwargs={"pk": user.pk})
    login_url = reverse("user:login")
    response = client.post(endpoint, data=form_data)

    assert response.status_code == 302
    assert response.url == f"{login_url}?next={endpoint}"


@pytest.mark.django_db
def test_user_update_view_get_other_user(authenticated_client, another_user):
    endpoint = reverse("user:update", kwargs={"pk": another_user.pk})
    response = authenticated_client.get(endpoint)

    assert response.status_code == 404


@pytest.mark.django_db
def test_user_update_view_post_other_user(authenticated_client, another_user):
    form_data = {
        "username": "another_user_updated",
        "email": "another_user_updated@example.com",
        "first_name": "taken_Test_updated",
        "last_name": "another_user_updated",
    }
    endpoint = reverse("user:update", kwargs={"pk": another_user.pk})
    response = authenticated_client.post(endpoint, data=form_data)

    assert response.status_code == 404

    another_user.refresh_from_db()
    assert another_user.username != "another_user_updated"
    assert another_user.email != "another_user_updated@example.com"


@pytest.mark.django_db
def test_user_update_view_another_username(authenticated_client, user, another_user):
    form_data = {
        "username": "anotheruser",
        "email": "testuser_updated@example.com",
        "first_name": "Test_updated",
        "last_name": "User_updated",
    }
    endpoint = reverse("user:update", kwargs={"pk": user.pk})
    response = authenticated_client.post(endpoint, data=form_data)
    form = response.context["user_update_form"]

    assert response.status_code == 200
    assert not form.is_valid()
    assert "username" in form.errors


@pytest.mark.django_db
def test_user_update_view_taken_email(authenticated_client, user, another_user):
    form_data = {
        "username": "testuser",
        "email": "another_user@example.com",
        "first_name": "Test_updated",
        "last_name": "User_updated",
    }
    endpoint = reverse("user:update", kwargs={"pk": user.pk})
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
    authenticated_client, user, missing_field, form_data
):
    endpoint = reverse("user:update", kwargs={"pk": user.pk})
    response = authenticated_client.post(endpoint, data=form_data)
    form = response.context["user_update_form"]

    assert response.status_code == 200
    assert not form.is_valid()
    assert missing_field in form.errors
