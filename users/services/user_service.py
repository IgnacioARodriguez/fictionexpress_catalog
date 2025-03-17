# users/services.py
from rest_framework_simplejwt.tokens import RefreshToken

class UserService:
    def __init__(self, user_repository):
        self.user_repository = user_repository  

    def authenticate_user(self, email, password):
        user = self.user_repository.get_user_by_email(email)
        if user is None:
            raise ValueError("User not found")
        if not user.check_password(password):
            raise ValueError("Invalid credentials")

        refresh = RefreshToken.for_user(user)
        return {'refresh': str(refresh), 'access': str(refresh.access_token)}
