import pytest
from django.contrib.messages import get_messages
from django.urls import reverse

from user.messages import LOGIN_SUCCESS
from user.views import UserLoginView


@pytest.mark.django_db
def test_user_login_view_get(client):
    endpoint = reverse("user:login")
    response = client.get(endpoint)

    assert response.status_code == 200
    assert "user/user_login.html" in [t.name for t in response.templates]


@pytest.mark.django_db
@pytest.mark.parametrize(
    "username, password",
    [
        ("testuser", "testpassword123"),
        ("testuser@example.com", "testpassword123"),
    ],
    ids=["username", "email"],
)
def test_user_login_view(client, test_user, username, password):
    form_data = {
        "username": username,
        "password": password,
    }
    endpoint = reverse("user:login")
    redirect_url = reverse("home:home_page")
    response = client.post(endpoint, data=form_data)

    assert response.status_code == 302
    assert response.url == redirect_url

    response = client.get(redirect_url)
    assert response.wsgi_request.user.is_authenticated


@pytest.mark.django_db
def test_user_login_view_success_message(client, test_user):
    form_data = {
        "username": "testuser",
        "password": "testpassword123",
    }
    endpoint = reverse("user:login")
    response = client.post(endpoint, data=form_data, follow=True)
    messages = list(get_messages(response.wsgi_request))

    assert any(LOGIN_SUCCESS in str(m) for m in messages)


@pytest.mark.django_db
def test_user_login_view_context(client):
    endpoint = reverse("user:login")
    response = client.get(endpoint)

    assert "login_form" in response.context


@pytest.mark.django_db
@pytest.mark.parametrize(
    "missing_field, form_data",
    [
        ("username", {"username": "", "password": "testpassword123"}),
        ("password", {"username": "testuser", "password": ""}),
    ],
    ids=["username", "password"],
)
def test_user_login_view_without_required_fields(
    client, test_user, missing_field, form_data
):
    endpoint = reverse("user:login")
    response = client.post(endpoint, data=form_data)
    form = response.context["login_form"]

    assert response.status_code == 200
    assert not form.is_valid()
    assert missing_field in form.errors


@pytest.mark.django_db
def test_user_login_view_with_wrong_password(client, test_user):
    form_data = {
        "username": "testuser",
        "password": "wrong_password",
    }
    endpoint = reverse("user:login")
    response = client.post(endpoint, data=form_data)
    form = response.context["form"]

    assert response.status_code == 200
    assert not form.is_valid()
    assert "__all__" in form.errors
    assert not response.wsgi_request.user.is_authenticated


@pytest.mark.django_db
@pytest.mark.parametrize(
    "username, password",
    [
        ("wrong_username", "testpassword123"),
        ("wrong@example.com", "testpassword123"),
    ],
    ids=["wrong_username", "wrong_email"],
)
def test_user_login_view_with_wrong_username(client, test_user, username, password):
    form_data = {
        "username": username,
        "password": password,
    }
    endpoint = reverse("user:login")
    response = client.post(endpoint, data=form_data)
    form = response.context["form"]

    assert response.status_code == 200
    assert not form.is_valid()
    assert "__all__" in form.errors
    assert not response.wsgi_request.user.is_authenticated


@pytest.mark.django_db
@pytest.mark.parametrize(
    "username, password",
    [
        ("testuser", ""),
        ("tesuser@example.com", ""),
    ],
    ids=["username_empty_password", "email_empty_password"],
)
def test_user_login_view_without_password(client, test_user, username, password):
    form_data = {
        "username": username,
        "password": password,
    }
    endpoint = reverse("user:login")
    response = client.post(endpoint, data=form_data)
    form = response.context["form"]

    assert response.status_code == 200
    assert not form.is_valid()
    assert "password" in form.errors
    assert not response.wsgi_request.user.is_authenticated
