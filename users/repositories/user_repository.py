import logging
from users.models import User

logger = logging.getLogger(__name__)
class UserRepository:
    """
    Repository to handle CRUD operations on the User model.
    """

    @staticmethod
    def get_user_by_email(email):
        """
        Retrieves a user by their email.

        :param email: Email of the user to search for.
        :return: User if exists, None if not exists.
        """
        try:
            user = User.objects.get(email=email)
            logger.info(f"User found by email: {email}")
            return user
        except User.DoesNotExist:
            logger.warning(f"User not found with email: {email}") 
            return None
        except Exception as e:
            logger.error(f"Unexpected error retrieving user by email {email}: {e}")
            return None

    @staticmethod
    def create_user(username, email, password, role="reader"):
        """
        Creates a new user in the database.

        :param username: Username.
        :param email: Email.
        :param password: User's password.
        :param role: User's role (default "reader").
        :return: Created user.
        :raises ValueError: If there is a problem with the provided data.
        :raises Exception: If an unexpected error occurs.
        """
        try:
            user = User.objects.create_user(username=username, email=email, password=password, role=role)
            logger.info(f"User created successfully: {email} (Role: {role})")
            return user
        except ValueError as e:
            logger.warning(f"Validation error while creating user {email}: {e}")
            raise ValueError(f"Error creating user: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error creating user {email}: {e}") 
            raise Exception(f"Unexpected error creating user: {str(e)}")

    @staticmethod
    def get_user_by_id(user_id):
        """
        Retrieves a user by their ID.

        :param user_id: User ID.
        :return: User if exists, None if not exists.
        """
        try:
            user = User.objects.filter(id=user_id).first()
            if user:
                logger.info(f"User retrieved by ID: {user_id}")  
            else:
                logger.warning(f"User not found with ID: {user_id}")  
            return user
        except Exception as e:
            logger.error(f"Unexpected error retrieving user by ID {user_id}: {e}")  
            return None

    @staticmethod
    def get_all_users():
        """
        Retrieves all users ordered by ID.

        :return: QuerySet with all users.
        """
        try:
            users = User.objects.all().order_by("id")
            logger.info(f"Retrieved {users.count()} users")
            return users
        except Exception as e:
            logger.error(f"Unexpected error retrieving all users: {e}") 
            return None

    @staticmethod
    def update_user(user, data):
        """
        Updates a user's data.

        :param user: Instance of the user to update.
        :param data: Dictionary with the fields to update.
        :return: Updated user.
        """
        try:
            for key, value in data.items():
                setattr(user, key, value)
            user.save()
            logger.info(f"User updated successfully: {user.email}")  
            return user
        except Exception as e:
            logger.error(f"Unexpected error updating user {user.email}: {e}") 
            return None

    @staticmethod
    def delete_user(user):
        """
        Deletes a user from the database.

        :param user: Instance of the user to delete.
        """
        try:
            email = user.email 
            user.delete()
            logger.info(f"User deleted successfully: {email}")  
        except Exception as e:
            logger.error(f"Unexpected error deleting user {email}: {e}") 
