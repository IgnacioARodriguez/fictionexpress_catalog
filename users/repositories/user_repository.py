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

    @staticmethod
    def get_user_by_id(user_id):
        return User.objects.filter(id=user_id).first()
    
    @staticmethod
    def get_all_users():
        return User.objects.all()
    
    @staticmethod
    def update_user(user, data):
        for key, value in data.items():
            setattr(user, key, value)

        user.save()
        return user
    
    @staticmethod
    def delete_user(user):
        user.delete()