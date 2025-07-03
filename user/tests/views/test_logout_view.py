import pytest
from django.contrib.messages import get_messages
from django.urls import reverse

from user.messages import LOGOUT_SUCCESS
from user.views import UserLogoutView


@pytest.mark.django_db
def test_logout_redirects(authenticated_client):
    endpoint = reverse("user:logout")
    response = authenticated_client.post(endpoint)

    assert response.status_code == 302
    assert response.url == reverse("home:home_page")
    assert not response.wsgi_request.user.is_authenticated


@pytest.mark.django_db
def test_logout_success_message(authenticated_client):
    endpoint = reverse("user:logout")
    response = authenticated_client.post(endpoint, follow=True)
    messages = list(get_messages(response.wsgi_request))

    assert any(LOGOUT_SUCCESS in str(m) for m in messages)
