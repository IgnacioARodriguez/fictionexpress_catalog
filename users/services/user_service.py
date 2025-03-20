from rest_framework_simplejwt.tokens import RefreshToken
from users.repositories.user_repository import UserRepository
from users.dtos.user_dto import UserDTO

class UserService:
    """
    Service layer for managing user operations such as authentication, 
    creation, retrieval, update, and deletion.
    """

    def __init__(self, user_repository=None):
        """
        Initializes the UserService with a repository instance.

        :param user_repository: An optional UserRepository instance.
        """
        self.user_repository = user_repository or UserRepository()

    def authenticate_user(self, email, password):
        """
        Authenticates a user based on email and password.

        :param email: User's email.
        :param password: User's password.
        :return: A dictionary containing access and refresh tokens.
        :raises ValueError: If the user is not found or credentials are invalid.
        """
        user = self.user_repository.get_user_by_email(email)
        if user is None:
            raise ValueError("User not found")
        if not user.check_password(password):
            raise ValueError("Invalid credentials")

        refresh = RefreshToken.for_user(user)
        return {'refresh': str(refresh), 'access': str(refresh.access_token)}
    
    def logout_user(self, refresh_token):
        """
        Logs out a user by blacklisting their refresh token.

        :param refresh_token: The refresh token to blacklist.
        :raises ValueError: If the token is invalid.
        """
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception:
            raise ValueError("Invalid token")
    
    def create_user(self, data):
        """
        Creates a new user.

        :param data: A dictionary containing user details such as username, email, password, and role.
        :return: A dictionary containing the created user's details along with JWT tokens.
        :raises ValueError: If the email is already registered.
        """
        existing_user = self.user_repository.get_user_by_email(data.get("email"))
        if existing_user:
            raise ValueError("The email is already registered")

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
        """
        Retrieves a user by ID.

        :param user_id: The ID of the user to retrieve.
        :return: The user object if found.
        :raises ValueError: If the user is not found.
        """
        user = self.user_repository.get_user_by_id(user_id)
        if not user:
            raise ValueError("User not found")

        return user
    
    def update_user(self, user_id, data):
        """
        Updates a user's information.

        :param user_id: The ID of the user to update.
        :param data: A dictionary containing the fields to update.
        :return: The updated user object.
        :raises ValueError: If the user is not found.
        """
        user = self.user_repository.get_user_by_id(user_id)
        if not user:
            raise ValueError("User not found")

        return self.user_repository.update_user(user, data)
    
    def delete_user(self, user_id):
        """
        Deletes a user by ID.

        :param user_id: The ID of the user to delete.
        :return: None
        :raises ValueError: If the user is not found.
        """
        user = self.user_repository.get_user_by_id(user_id)
        if not user:
            raise ValueError("User not found")

        return self.user_repository.delete_user(user)
    
    def get_all_users(self):
        """
        Retrieves all users.

        :return: A queryset containing all users.
        """
        return self.user_repository.get_all_users()
