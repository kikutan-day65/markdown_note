import pytest
from django.core import mail
from django.urls import reverse


@pytest.mark.django_db
def test_password_reset_view_get(client):
    endpoint = reverse("user:password_reset")
    response = client.get(endpoint)

    assert response.status_code == 200
    assert "user/user_password_reset.html" in [t.name for t in response.templates]


@pytest.mark.django_db
def test_password_reset_view_context(client):
    endpoint = reverse("user:password_reset")
    response = client.get(endpoint)

    assert "password_reset_form" in response.context


@pytest.mark.django_db
def test_password_reset_view_post(client, test_user):
    form_data = {
        "email": test_user.email,
    }
    endpoint = reverse("user:password_reset")
    redirect_endpoint = reverse("user:password_reset_done")
    response = client.post(endpoint, data=form_data)

    assert response.status_code == 302
    assert response.url == redirect_endpoint

    assert len(mail.outbox) == 1
    email = mail.outbox[0]
    assert test_user.email in email.to
    assert "Reset Your Password on" in email.subject


@pytest.mark.django_db
def test_password_reset_view_without_required_field(client):
    form_data = {
        "email": "",
    }
    endpoint = reverse("user:password_reset")
    response = client.post(endpoint, data=form_data)
    form = response.context["password_reset_form"]

    assert response.status_code == 200
    assert not form.is_valid()
    assert "email" in form.errors
