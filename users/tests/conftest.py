import pytest
from users.models import User
from django.conf import settings
from rest_framework.test import APIClient
import django

# @pytest.fixture(scope="session", autouse=True)
# def setup_django():
#     """Configura Django antes de correr los tests"""
#     if not settings.configured:
#         django.setup()

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
