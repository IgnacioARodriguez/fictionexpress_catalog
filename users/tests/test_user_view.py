from django.urls import reverse
import pytest

@pytest.mark.django_db
def test_list_users_as_admin(api_client, create_admin_user):
    """Test to list users as an admin"""
    api_client.force_authenticate(user=create_admin_user)

    url = reverse("user-list")
    response = api_client.get(url)

    assert response.status_code == 200
    assert "results" in response.data

@pytest.mark.django_db
def test_list_users_as_reader(api_client, create_test_user):
    """Test to list users as a reader"""
    api_client.force_authenticate(user=create_test_user)

    url = reverse("user-list")
    response = api_client.get(url)

    assert response.status_code == 403

@pytest.mark.django_db
def test_create_user(api_client):
    """Test to create a new user"""
    url = reverse("user-list")
    data = {
        "username": "newuser",
        "email": "newuser@example.com",
        "password": "securepassword",
        "role": "reader"
    }
    response = api_client.post(url, data, format="json")

    assert response.status_code == 201
    assert response.data["email"] == "newuser@example.com"

@pytest.mark.django_db
def test_authenticate_user(api_client, create_test_user):
    """Test to authenticate a user"""
    url = reverse("user-login")
    data = {
        "email": create_test_user.email,
        "password": 'testpassword'
    }
    response = api_client.post(url, data, format="json")

    print(response.data)

    assert response.status_code == 200
    assert "access" in response.data
    assert "refresh" in response.data

@pytest.mark.django_db
def test_update_user(api_client, create_test_user):
    """Test to update a user"""
    api_client.force_authenticate(user=create_test_user)

    url = reverse("user-detail", args=[create_test_user.id])
    data = {"username": "updateduser"}

    response = api_client.put(url, data, format="json")

    assert response.status_code == 200
    assert response.data["username"] == "updateduser"

@pytest.mark.django_db
def test_delete_user_as_admin(api_client, create_admin_user, create_test_user):
    """Test to delete a user as an admin"""
    api_client.force_authenticate(user=create_admin_user)

    url = reverse("user-detail", args=[create_test_user.id])
    response = api_client.delete(url)

    assert response.status_code == 204

@pytest.mark.django_db
def test_get_user_by_id(api_client, create_test_user):
    """Test to get a user by ID"""
    api_client.force_authenticate(user=create_test_user)

    url = reverse("user-detail", args=[create_test_user.id])
    response = api_client.get(url)

    assert response.status_code == 200
    assert response.data["id"] == create_test_user.id
    assert response.data["email"] == create_test_user.email