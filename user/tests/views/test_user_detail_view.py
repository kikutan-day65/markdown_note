import pytest
from django.urls import reverse

from user.views import UserDetailView


@pytest.mark.django_db
def test_user_detail_view(client, test_user):
    endpoint = reverse("user:detail", kwargs={"pk": test_user.pk})
    response = client.get(endpoint)

    assert response.status_code == 200
    assert "user/user_detail.html" in [t.name for t in response.templates]
    assert response.context["user_detail"] == test_user


@pytest.mark.django_db
def test_user_detail_view_nonexistent_user(client):
    dummy_pk = 999
    endpoint = reverse("user:detail", kwargs={"pk": dummy_pk})
    response = client.get(endpoint)

    assert response.status_code == 404
