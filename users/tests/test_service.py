import pytest
from unittest.mock import MagicMock, patch
from users.services.user_service import UserService
from users.repositories.user_repository import UserRepository
from users.models import User

@pytest.fixture
def mock_user_repository():
    mock_repo = MagicMock(spec=UserRepository)
    return mock_repo

@patch("users.services.user_service.RefreshToken")
def test_create_user(mock_refresh_token, mock_user_repository):
    user_data = {
        "username": "newuser",
        "email": "newuser@example.com",
        "password": "securepassword",
        "role": "reader",
    }

    mock_user_repository.create_user.return_value = MagicMock(
        id=1,
        username=user_data["username"],
        email=user_data["email"],
        role=user_data["role"],
    )

    mock_user_repository.get_user_by_email.return_value = None

    mock_refresh_instance = MagicMock()
    mock_refresh_instance.access_token = "mock_access_token"
    mock_refresh_token.for_user.return_value = mock_refresh_instance

    user_service = UserService(mock_user_repository) 

    user = user_service.create_user(user_data)

    mock_user_repository.create_user.assert_called_once_with(
        username="newuser",
        email="newuser@example.com",
        password="securepassword",
        role="reader",
    )

    assert user["email"] == "newuser@example.com"
    assert user["role"] == "reader"


@patch("users.services.user_service.RefreshToken") 
def test_authenticate_user(mock_refresh_token, mock_user_repository):
    user_mock = MagicMock()
    user_mock.id = 1
    user_mock.username = "testuser"
    user_mock.email = "test@example.com"
    user_mock.role = "reader"
    user_mock.check_password.return_value = True

    mock_user_repository.get_user_by_email.return_value = user_mock

    mock_refresh_instance = MagicMock()
    mock_refresh_instance.access_token = "mock_access_token"
    mock_refresh_token.for_user.return_value = mock_refresh_instance

    user_service = UserService(user_repository=mock_user_repository)

    token_data = user_service.authenticate_user("test@example.com", "securepassword")

    mock_user_repository.get_user_by_email.assert_called_once_with("test@example.com")
    mock_refresh_token.for_user.assert_called_once_with(user_mock) 

    assert token_data["access"] == "mock_access_token"
    assert "refresh" in token_data 


    
def test_get_user_by_id(mock_user_repository):
    mock_user = MagicMock(id=1, username="testuser", email="test@example.com")
    mock_user_repository.get_user_by_id.return_value = mock_user

    user_service = UserService(user_repository=mock_user_repository)
    user = user_service.get_user_by_id(1)

    mock_user_repository.get_user_by_id.assert_called_once_with(1)
    assert user.email == "test@example.com"


def test_update_user(mock_user_repository):
    mock_user = MagicMock(id=1, username="olduser", email="old@example.com")
    mock_user_repository.get_user_by_id.return_value = mock_user
    mock_user_repository.update_user.return_value = mock_user

    user_service = UserService(user_repository=mock_user_repository)
    updated_user = user_service.update_user(1, {"username": "newuser"})

    mock_user_repository.update_user.assert_called_once()
    assert updated_user.username == "olduser"


def test_delete_user(mock_user_repository):
    mock_user = MagicMock(id=1)
    mock_user_repository.get_user_by_id.return_value = mock_user

    user_service = UserService(user_repository=mock_user_repository)
    user_service.delete_user(1)

    mock_user_repository.delete_user.assert_called_once_with(mock_user)


@patch("users.services.user_service.RefreshToken")
def test_logout_user(mock_refresh_token):
    mock_refresh_instance = MagicMock()
    mock_refresh_token.return_value = mock_refresh_instance

    user_service = UserService()
    user_service.logout_user("mock_refresh_token")

    mock_refresh_instance.blacklist.assert_called_once()