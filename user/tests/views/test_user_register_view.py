import pytest
from django.contrib.messages import get_messages
from django.urls import reverse

from user.messages import REGISTER_SUCCESS
from user.views import UserRegisterView


@pytest.mark.django_db
def test_user_register_view_get(client):
    response = client.get(reverse("user:register"))

    assert response.status_code == 200
    assert "user/user_register.html" in [t.name for t in response.templates]


@pytest.mark.django_db
def test_user_register_view_post(client):
    form_data = {
        "username": "testuser",
        "email": "testuser@example.com",
        "password1": "testpassword123",
        "password2": "testpassword123",
        "first_name": "Test",
        "last_name": "User",
    }
    endpoint = reverse("user:register")
    response = client.post(endpoint, data=form_data)

    assert response.status_code == 302
    assert response.url == reverse("user:login")


@pytest.mark.django_db
def test_user_register_view_success_message(client):
    form_data = {
        "username": "testuser",
        "email": "testuser@example.com",
        "password1": "testpassword123",
        "password2": "testpassword123",
        "first_name": "Test",
        "last_name": "User",
    }
    endpoint = reverse("user:register")
    response = client.post(endpoint, data=form_data, follow=True)
    messages = list(get_messages(response.wsgi_request))

    assert any(REGISTER_SUCCESS in str(m) for m in messages)


@pytest.mark.django_db
def test_user_register_view_context(client):
    endpoint = reverse("user:register")
    response = client.get(endpoint)

    assert "register_form" in response.context


@pytest.mark.django_db
@pytest.mark.parametrize(
    "missing_field, form_data",
    [
        (
            "username",
            {
                "username": "",
                "email": "testuser@example.com",
                "password1": "testpassword123",
                "password2": "testpassword123",
                "first_name": "Test",
                "last_name": "User",
            },
        ),
        (
            "email",
            {
                "username": "testuser",
                "email": "",
                "password1": "testpassword123",
                "password2": "testpassword123",
                "first_name": "Test",
                "last_name": "User",
            },
        ),
        (
            "password1",
            {
                "username": "testuser",
                "email": "testuser@example.com",
                "password1": "",
                "password2": "testpassword123",
                "first_name": "Test",
                "last_name": "User",
            },
        ),
        (
            "password2",
            {
                "username": "testuser",
                "email": "testuser@example.com",
                "password1": "testpassword123",
                "password2": "",
                "first_name": "Test",
                "last_name": "User",
            },
        ),
        (
            "first_name",
            {
                "username": "testuser",
                "email": "testuser@example.com",
                "password1": "testpassword123",
                "password2": "testpassword123",
                "first_name": "",
                "last_name": "User",
            },
        ),
        (
            "last_name",
            {
                "username": "testuser",
                "email": "testuser@example.com",
                "password1": "testpassword123",
                "password2": "testpassword123",
                "first_name": "Test",
                "last_name": "",
            },
        ),
    ],
    ids=[
        "missing_username",
        "missing_email",
        "missing_password1",
        "missing_password2",
        "missing_first_name",
        "missing_last_name",
    ],
)
def test_user_register_view_post_without_required_fields(
    client, missing_field, form_data
):
    endpoint = reverse("user:register")
    response = client.post(endpoint, data=form_data)
    form = response.context["form"]

    assert response.status_code == 200
    assert not form.is_valid()
    assert missing_field in form.errors


@pytest.mark.django_db
def test_user_register_view_duplicate_username(client, test_user):
    form_data = {
        "username": "testuser",
        "email": "testuser@example.com",
        "password1": "testpassword123",
        "password2": "testpassword123",
        "first_name": "Test",
        "last_name": "User",
    }
    endpoint = reverse("user:register")
    response = client.post(endpoint, data=form_data)
    form = response.context["form"]

    assert response.status_code == 200
    assert not form.is_valid()
    assert "username" in form.errors


@pytest.mark.django_db
def test_user_register_view_duplicate_email(client, test_user):
    form_data = {
        "username": "another_testuser",
        "email": "testuser@example.com",
        "password1": "testpassword123",
        "password2": "testpassword123",
        "first_name": "Test",
        "last_name": "User",
    }
    endpoint = reverse("user:register")
    response = client.post(endpoint, data=form_data)
    form = response.context["form"]

    assert response.status_code == 200
    assert not form.is_valid()
    assert "email" in form.errors


@pytest.mark.django_db
def test_user_register_view_password_mismatch(client):
    form_data = {
        "username": "testuser",
        "email": "testuser@example.com",
        "password1": "testpassword123",
        "password2": "testpassword123456",
        "first_name": "Test",
        "last_name": "User",
    }
    endpoint = reverse("user:register")
    response = client.post(endpoint, data=form_data)
    form = response.context["form"]

    assert response.status_code == 200
    assert not form.is_valid()
    assert "password2" in form.errors
