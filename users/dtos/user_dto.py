# users/dto.py
from rest_framework import serializers
from users.models import User

class UserDTO(serializers.ModelSerializer):
    refresh = serializers.CharField()
    access = serializers.CharField()

    class Meta:
        model = User
        fields = ["id", "username", "email", "role", "refresh", "access"]
