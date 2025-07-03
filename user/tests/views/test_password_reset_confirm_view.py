from unittest.mock import patch

import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

CustomUser = get_user_model()


@pytest.mark.django_db
def test_password_reset_confirm_view_get(client, test_user):
    uidb64 = urlsafe_base64_encode(force_bytes(test_user.pk))
    token = default_token_generator.make_token(test_user)
    endpoint = reverse(
        "user:password_reset_confirm",
        kwargs={"uidb64": uidb64, "token": token},
    )
    response = client.get(endpoint, follow=True)

    assert response.status_code == 200
    assert "user/user_password_reset_confirm.html" in [
        t.name for t in response.templates
    ]


@pytest.mark.django_db
def test_password_reset_confirm_view_context(client, test_user):
    uidb64 = urlsafe_base64_encode(force_bytes(test_user.pk))
    token = default_token_generator.make_token(test_user)
    endpoint = reverse(
        "user:password_reset_confirm",
        kwargs={"uidb64": uidb64, "token": token},
    )
    response = client.get(endpoint, follow=True)

    assert "password_reset_confirm_form" in response.context


@pytest.mark.django_db
def test_password_reset_confirm_success(client, test_user):
    uidb64 = urlsafe_base64_encode(force_bytes(test_user.pk))
    token = default_token_generator.make_token(test_user)

    endpoint = reverse(
        "user:password_reset_confirm",
        kwargs={"uidb64": uidb64, "token": token},
    )
    form_data = {
        "new_password1": "newTestPassword123",
        "new_password2": "newTestPassword123",
    }

    response_get = client.get(endpoint, follow=True)
    response_post = client.post(response_get.request["PATH_INFO"], data=form_data)

    test_user.refresh_from_db()
    assert test_user.check_password("newTestPassword123")

    login_endpoint = reverse("user:login")
    login_data = {"username": "testuser", "password": "newTestPassword123"}
    login_response = client.post(login_endpoint, data=login_data)

    assert login_response.wsgi_request.user.is_authenticated


@pytest.mark.django_db
def test_password_reset_confirm_redirect(client, test_user):
    uidb64 = urlsafe_base64_encode(force_bytes(test_user.pk))
    token = default_token_generator.make_token(test_user)

    endpoint = reverse(
        "user:password_reset_confirm",
        kwargs={"uidb64": uidb64, "token": token},
    )
    form_data = {
        "new_password1": "newTestPassword123",
        "new_password2": "newTestPassword123",
    }

    response_get = client.get(endpoint, follow=True)
    response_post = client.post(response_get.request["PATH_INFO"], data=form_data)
    expected_url = reverse("user:password_reset_complete")

    assert response_post.status_code == 302
    assert response_post["Location"] == expected_url


@pytest.mark.django_db
def test_password_reset_confirm_invalid_token(client, test_user):
    uidb64 = urlsafe_base64_encode(force_bytes(test_user.pk))
    invalid_token = "invalid-token"
    endpoint = reverse(
        "user:password_reset_confirm",
        kwargs={"uidb64": uidb64, "token": invalid_token},
    )
    response = client.get(endpoint)

    assert response.status_code == 200
    assert response.context["validlink"] is False


@pytest.mark.django_db
def test_password_reset_confirm_mismatch_password(client, test_user):
    uidb64 = urlsafe_base64_encode(force_bytes(test_user.pk))
    token = default_token_generator.make_token(test_user)

    endpoint = reverse(
        "user:password_reset_confirm",
        kwargs={"uidb64": uidb64, "token": token},
    )
    form_data = {
        "new_password1": "newTestPassword123",
        "new_password2": "mismatchedPassword123",
    }

    response_get = client.get(endpoint, follow=True)
    response_post = client.post(response_get.request["PATH_INFO"], data=form_data)

    assert response_post.status_code == 200

    form = response_post.context.get("form")
    assert not form.is_valid()
    assert "new_password2" in form.errors

    test_user.refresh_from_db()
    assert not test_user.check_password("newTestPassword123")


@pytest.mark.django_db
def test_password_reset_confirm_weak_password(client, test_user):
    uidb64 = urlsafe_base64_encode(force_bytes(test_user.pk))
    token = default_token_generator.make_token(test_user)

    endpoint = reverse(
        "user:password_reset_confirm",
        kwargs={"uidb64": uidb64, "token": token},
    )
    form_data = {
        "new_password1": "abc",
        "new_password2": "abc",
    }

    response_get = client.get(endpoint, follow=True)
    response_post = client.post(response_get.request["PATH_INFO"], data=form_data)

    assert response_post.status_code == 200
    assert "form" in response_post.context

    form = response_post.context["password_reset_confirm_form"]
    assert "new_password2" in form.errors


@pytest.mark.django_db
@pytest.mark.parametrize(
    "error_field, form_data",
    [
        ("new_password1", {"new_password1": "", "new_password2": "newTestPassword123"}),
        ("new_password2", {"new_password1": "newTestPassword123", "new_password2": ""}),
        ("new_password2", {"new_password1": "", "new_password2": ""}),
    ],
    ids=["new_password1", "new_password2", "new_password1 and new_password2"],
)
def test_password_reset_confirm_without_required_fields(
    client, test_user, error_field, form_data
):
    uidb64 = urlsafe_base64_encode(force_bytes(test_user.pk))
    token = default_token_generator.make_token(test_user)

    endpoint = reverse(
        "user:password_reset_confirm",
        kwargs={"uidb64": uidb64, "token": token},
    )

    response_get = client.get(endpoint, follow=True)
    response_post = client.post(response_get.request["PATH_INFO"], data=form_data)
    form = response_post.context["password_reset_confirm_form"]

    assert response_post.status_code == 200
    assert error_field in form.errors
