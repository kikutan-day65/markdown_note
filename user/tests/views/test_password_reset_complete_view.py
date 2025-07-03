import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_password_reset_complete_view(client):
    url = reverse("user:password_reset_complete")
    response = client.get(url)

    assert response.status_code == 200
    assert "user/user_password_reset_complete.html" in [
        t.name for t in response.templates
    ]
