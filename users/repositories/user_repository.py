# users/repository.py
from django.core.exceptions import ObjectDoesNotExist
from users.models import User

class UserRepository:

    @staticmethod
    def get_user_by_email(email):
            try:
                return User.objects.get(email=email)
            except Exception as e:
                return None

    @staticmethod
    def create_user(username, email, password, role="reader"):
        try:
            return User.objects.create_user(username=username, email=email, password=password, role=role)
        except ValueError as e:
            raise 
        except Exception as e:
            raise