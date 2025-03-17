# users/repository.py
from django.core.exceptions import ObjectDoesNotExist
from users.models import User

class UserRepository:
    @staticmethod
    def get_user_by_email(email):
        try:
            return User.objects.get(email=email)
        except ObjectDoesNotExist:
            return None
