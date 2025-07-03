import pytest
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.urls import reverse

from user.messages import ACCOUNT_DELETE_SUCCESS

CustomUser = get_user_model()


@pytest.mark.django_db
def test_user_delete_view(authenticated_client, test_user):
    endpoint = reverse("user:delete_user", kwargs={"pk": test_user.pk})
    response = authenticated_client.get(endpoint)

    assert response.status_code == 200


@pytest.mark.django_db
def test_user_delete_view_success(authenticated_client, test_user):
    endpoint = reverse("user:delete_user", kwargs={"pk": test_user.pk})
    response = authenticated_client.post(endpoint, follow=True)

    assert response.status_code == 200
    assert not CustomUser.objects.filter(pk=test_user.pk).exists()


@pytest.mark.django_db
def test_user_delete_view_success_message(authenticated_client, test_user):
    endpoint = reverse("user:delete_user", kwargs={"pk": test_user.pk})
    response = authenticated_client.post(endpoint, follow=True)
    messages = list(get_messages(response.wsgi_request))

    assert any(ACCOUNT_DELETE_SUCCESS in str(m) for m in messages)


@pytest.mark.django_db
def test_user_delete_view_context(authenticated_client, test_user):
    endpoint = reverse("user:delete_user", kwargs={"pk": test_user.pk})
    response = authenticated_client.get(endpoint)

    assert response.status_code == 200
    assert response.context.get("user_delete") is True


@pytest.mark.django_db
def test_user_delete_view_get_unauthorized_user(client, test_user):
    endpoint = reverse("user:delete_user", kwargs={"pk": test_user.pk})
    login_url = reverse("user:login")
    response = client.get(endpoint)

    assert response.status_code == 302
    assert response.url == f"{login_url}?next={endpoint}"


@pytest.mark.django_db
def test_user_delete_view_post_unauthenticated_user(client, test_user):
    endpoint = reverse("user:delete_user", kwargs={"pk": test_user.pk})
    login_url = reverse("user:login")

    response = client.post(endpoint)

    assert response.status_code == 302
    assert response.url == f"{login_url}?next={endpoint}"


@pytest.mark.django_db
def test_user_cannot_get_another_users_delete_page(authenticated_client, taken_user):
    endpoint = reverse("user:delete_user", kwargs={"pk": taken_user.pk})
    response = authenticated_client.get(endpoint)

    assert response.status_code == 404


@pytest.mark.django_db
def test_user_cannot_post_another_users_delete(authenticated_client, taken_user):
    endpoint = reverse("user:delete_user", kwargs={"pk": taken_user.pk})
    response = authenticated_client.post(endpoint)

    assert response.status_code == 404
