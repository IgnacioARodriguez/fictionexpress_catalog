# users/services.py
from rest_framework_simplejwt.tokens import RefreshToken
from users.repositories.user_repository import UserRepository
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from users.dtos.user_dto import UserDTO

class UserService:
    def __init__(self, user_repository):
        self.user_repository = user_repository  

    @staticmethod
    def authenticate_user(self, email, password):
        user = UserRepository.get_user_by_email(email)
        if user is None:
            raise ValueError("User not found")
        if not user.check_password(password):
            raise ValueError("Invalid credentials")

        refresh = RefreshToken.for_user(user)
        return {'refresh': str(refresh), 'access': str(refresh.access_token)}
    
    @staticmethod
    def create_user(data):
        existing_user = UserRepository.get_user_by_email(data.get("email"))
        if existing_user:
            raise ValueError("El email ya está registrado")

        user = UserRepository.create_user(
            username=data["username"],
            email=data["email"],
            password=data["password"],
            role=data.get("role", "reader"),
        )

        refresh = RefreshToken.for_user(user)
        user_data = UserDTO(
            {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role": user.role,
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
        ).data

        return user_data
