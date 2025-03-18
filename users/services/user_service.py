from rest_framework_simplejwt.tokens import RefreshToken
from users.repositories.user_repository import UserRepository
from users.dtos.user_dto import UserDTO

class UserService:

    @staticmethod
    def authenticate_user(email, password):
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
    
    @staticmethod
    def get_user_by_id(user_id):
        user = UserRepository.get_user_by_id(user_id)
        if not user:
            raise ValueError("Usuario no encontrado")

        return user
    
    @staticmethod
    def update_user(user_id, data):
        user = UserRepository.get_user_by_id(user_id)
        if not user:
            raise ValueError("Usuario no encontrado")

        return UserRepository.update_user(user, data)
    
    @staticmethod
    def delete_user(user_id):
        user = UserRepository.get_user_by_id(user_id)
        if not user:
            raise ValueError("Usuario no encontrado")

        return UserRepository.delete_user(user)
    
    @staticmethod
    def get_all_users():
        return UserRepository.get_all_users()
