import pytest
from users.models import User
from django.conf import settings
from rest_framework.test import APIClient
import django
@pytest.fixture
def api_client():
    """Create an instance of the Django test client."""
    return APIClient()

@pytest.fixture
def create_test_user(db):
    """Create a test user."""
    return User.objects.create_user(
        username="testuser",
        email="testuser@example.com",
        password="testpassword",
        role="reader"
    )

@pytest.fixture
def create_admin_user(db):
    """Create an admin user."""
    return User.objects.create_superuser(
        username="admin",
        email="admin@example.com",
        password="adminpassword",
    )
