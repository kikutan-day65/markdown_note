import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_password_reset_done_view(client):
    endpoint = reverse("user:password_reset_done")
    response = client.get(endpoint)

    assert response.status_code == 200
    assert "user/user_password_reset_done.html" in [t.name for t in response.templates]
