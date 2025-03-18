import pytest
from users.models import User
from django.conf import settings
from rest_framework.test import APIClient

@pytest.fixture
def api_client():
    """Crea un cliente de API para hacer requests en los tests"""
    return APIClient()

@pytest.fixture
def create_test_user(db):
    return User.objects.create_user(
        username="testuser",
        email="testuser@example.com",
        password="testpassword",
        role="reader"
    )

@pytest.fixture
def create_admin_user(db):
    return User.objects.create_superuser(
        username="admin",
        email="admin@example.com",
        password="adminpassword",
    )

@pytest.fixture(autouse=True)
def print_db():
    print(f"Base de datos usada para los tests: {settings.DATABASES['default']['ENGINE']}")
