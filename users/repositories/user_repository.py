from users.models import User

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
            return User.objects.get(email=email)

        except User.DoesNotExist:
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
            return User.objects.create_user(username=username, email=email, password=password, role=role)

        except ValueError as e:
            raise ValueError(f"Error creating user: {str(e)}")
        except Exception as e:
            raise Exception(f"Unexpected error creating user: {str(e)}")

    @staticmethod
    def get_user_by_id(user_id):
        """
        Retrieves a user by their ID.

        :param user_id: User ID.
        :return: User if exists, None if not exists.
        """
        return User.objects.filter(id=user_id).first()

    @staticmethod
    def get_all_users():
        """
        Retrieves all users ordered by ID.

        :return: QuerySet with all users.
        """
        return User.objects.all().order_by("id")

    @staticmethod
    def update_user(user, data):
        """
        Updates a user's data.

        :param user: Instance of the user to update.
        :param data: Dictionary with the fields to update.
        :return: Updated user.
        """
        for key, value in data.items():
            setattr(user, key, value)
        user.save()
        return user

    @staticmethod
    def delete_user(user):
        """
        Deletes a user from the database.

        :param user: Instance of the user to delete.
        """
        user.delete()
