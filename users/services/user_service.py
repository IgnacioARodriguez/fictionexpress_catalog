from rest_framework_simplejwt.tokens import RefreshToken
from users.repositories.user_repository import UserRepository
from users.dtos.user_dto import UserDTO

class UserService:
    def __init__(self, user_repository=None):
        self.user_repository = user_repository or UserRepository()

    def authenticate_user(self, email, password):
        user = self.user_repository.get_user_by_email(email) 
        if user is None:
            raise ValueError("User not found")
        if not user.check_password(password):
            raise ValueError("Invalid credentials")

        refresh = RefreshToken.for_user(user)

        return {'refresh': str(refresh), 'access': str(refresh.access_token)}
    
    def logout_user(self, refresh_token):
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception as e:
            raise ValueError("Invalid token")
    
    def create_user(self, data):
        existing_user = self.user_repository.get_user_by_email(data.get("email"))
        if existing_user:
            raise ValueError("El email ya está registrado")

        user = self.user_repository.create_user(
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
    
    def get_user_by_id(self, user_id):
        user = self.user_repository.get_user_by_id(user_id)
        if not user:
            raise ValueError("Usuario no encontrado")

        return user
    
    def update_user(self, user_id, data):
        user = self.user_repository.get_user_by_id(user_id)
        if not user:
            raise ValueError("Usuario no encontrado")

        return self.user_repository.update_user(user, data)
    
    def delete_user(self, user_id):
        user = self.user_repository.get_user_by_id(user_id)
        if not user:
            raise ValueError("Usuario no encontrado")

        return self.user_repository.delete_user(user)
    
    def get_all_users(self):
        return self.user_repository.get_all_users()
