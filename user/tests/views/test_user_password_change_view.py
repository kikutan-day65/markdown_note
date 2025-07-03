import pytest
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.urls import reverse

from user.messages import PASSWORD_CHANGE_SUCCESS

CustomUser = get_user_model()


@pytest.mark.django_db
def test_user_password_change_view(authenticated_client):
    endpoint = reverse("user:change_password")
    response = authenticated_client.get(endpoint)

    assert response.status_code == 200


@pytest.mark.django_db
def test_password_change_success(authenticated_client, test_user):
    form_data = {
        "old_password": "testpassword123",
        "new_password1": "newpassword123",
        "new_password2": "newpassword123",
    }
    endpoint = reverse("user:change_password")
    redirect_url = reverse("user:detail", kwargs={"pk": test_user.pk})
    response = authenticated_client.post(endpoint, data=form_data)

    assert response.status_code == 302
    assert response.url == redirect_url

    logout_endpoint = reverse("user:logout")
    authenticated_client.post(logout_endpoint)

    login_endpoint = reverse("user:login")

    login_data = {"username": "testuser", "password": "newpassword123"}
    login_response = authenticated_client.post(
        login_endpoint, data=login_data, follow=True
    )

    assert login_response.wsgi_request.user.is_authenticated


@pytest.mark.django_db
def test_user_password_change_view_success_message(authenticated_client):
    form_data = {
        "old_password": "testpassword123",
        "new_password1": "newpassword123",
        "new_password2": "newpassword123",
    }
    endpoint = reverse("user:change_password")
    response = authenticated_client.post(endpoint, data=form_data)
    messages = list(get_messages(response.wsgi_request))

    assert response.status_code == 302
    assert any(PASSWORD_CHANGE_SUCCESS in str(m) for m in messages)


@pytest.mark.django_db
def test_user_password_change_view_get_unauthenticated_user(client):
    endpoint = reverse("user:change_password")
    login_url = reverse("user:login")
    response = client.get(endpoint)

    assert response.status_code == 302
    assert response.url == f"{login_url}?next={endpoint}"


@pytest.mark.django_db
def test_user_password_change_view_post_unauthenticated_user(client):
    endpoint = reverse("user:change_password")
    login_url = reverse("user:login")
    response = client.post(endpoint)

    assert response.status_code == 302
    assert response.url == f"{login_url}?next={endpoint}"


@pytest.mark.django_db
def test_user_password_change_view_incorrect_old_password(authenticated_client):
    form_data = {
        "old_password": "wrong_old_password123",
        "new_password1": "newpassword123",
        "new_password2": "newpassword123",
    }
    endpoint = reverse("user:change_password")
    response = authenticated_client.post(endpoint, data=form_data)
    form = response.context["password_change_form"]

    assert response.status_code == 200
    assert not form.is_valid()
    assert "old_password" in form.errors


@pytest.mark.django_db
def test_user_password_change_view_mismatched_new_password(authenticated_client):
    form_data = {
        "old_password": "testpassword123",
        "new_password1": "newpassword123",
        "new_password2": "mismatched_new_password123",
    }
    endpoint = reverse("user:change_password")
    response = authenticated_client.post(endpoint, data=form_data)
    form = response.context["password_change_form"]

    assert response.status_code == 200
    assert not form.is_valid()
    assert "new_password2" in form.errors
