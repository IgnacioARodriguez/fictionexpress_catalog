from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from users.serializers.user_serializer import UserSerializer
from users.services.user_service import UserService
from users.models import User
from rest_framework.pagination import PageNumberPagination
from users.docs import (
    list_users_docs, get_user_by_id_docs, create_user_docs,
    update_user_docs, delete_user_docs, login_user_docs, logout_user_docs
)

class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing user-related operations including authentication, 
    registration, retrieval, updating, and deletion.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    user_service = UserService()

    @login_user_docs
    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def login(self, request):
        """
        Authenticates a user and returns access and refresh tokens.

        :param request: The HTTP request containing email and password.
        :return: A JSON response with access and refresh tokens.
        :raises Exception: If authentication fails.
        """
        try:
            token_data = self.user_service.authenticate_user(
                email=request.data.get('email'), password=request.data.get('password')
            )
            return Response(token_data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @create_user_docs
    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def signup(self, request):
        """
        Registers a new user.

        :param request: The HTTP request containing user data.
        :return: A JSON response with the created user's details.
        :raises Exception: If the user creation fails.
        """
        try:
            serializer = UserSerializer(data=request.data)

            if serializer.is_valid():
                user_data = self.user_service.create_user(serializer.validated_data)
                return Response(user_data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @logout_user_docs
    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def logout(self, request):
        """
        Logs out the user by blacklisting the provided refresh token.

        :param request: The HTTP request containing the refresh token.
        :return: A JSON response confirming logout.
        :raises Exception: If the token is invalid.
        """
        try:
            refresh_token = request.data.get('refresh')
            self.user_service.logout_user(refresh_token)
            return Response({"message": "Logged out"}, status=status.HTTP_200_OK)
    
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @list_users_docs
    def list(self, request):
        """
        Lists all users (Admin only).

        :param request: The HTTP request.
        :return: A paginated list of users.
        :raises Exception: If an unexpected error occurs.
        """
        if not request.user.is_staff:
            return Response({"error": "You do not have permission"}, status=status.HTTP_403_FORBIDDEN)

        try:
            users = self.user_service.get_all_users()

            if not users.exists():
                return Response({"message": "No users available"}, status=status.HTTP_204_NO_CONTENT)

            paginator = PageNumberPagination()
            paginated_users = paginator.paginate_queryset(users, request)
            return paginator.get_paginated_response(UserSerializer(paginated_users, many=True).data)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @get_user_by_id_docs
    def retrieve(self, request, pk=None):
        """
        Retrieves a user by ID (Admins or the user themselves).

        :param request: The HTTP request.
        :param pk: The ID of the user.
        :return: The user details in JSON format.
        :raises ValueError: If the user is not found.
        :raises Exception: If an unexpected error occurs.
        """
        try:
            user = self.user_service.get_user_by_id(pk)
            if not request.user.is_staff and request.user.id != user.id:
                return Response({"error": "You do not have permission"}, status=status.HTTP_403_FORBIDDEN)
            else:
                return Response(UserSerializer(user).data)

        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @update_user_docs
    def update(self, request, pk=None):
        """
        Updates a user's details (Only the account owner).

        :param request: The HTTP request containing the new user data.
        :param pk: The ID of the user to update.
        :return: The updated user details.
        :raises ValueError: If the user is not found.
        :raises Exception: If an unexpected error occurs.
        """
        if request.user.id != int(pk):
            return Response({"error": "You do not have permission"}, status=status.HTTP_403_FORBIDDEN)

        try:
            user = self.user_service.update_user(pk, request.data)
            return Response(UserSerializer(user).data)

        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @delete_user_docs
    def destroy(self, request, pk=None):
        """
        Deletes a user (Admin only).

        :param request: The HTTP request.
        :param pk: The ID of the user to delete.
        :return: A JSON response confirming deletion.
        :raises ValueError: If the user is not found.
        :raises Exception: If an unexpected error occurs.
        """
        if not request.user.is_staff:
            return Response({"error": "You do not have permission"}, status=status.HTTP_403_FORBIDDEN)

        try:
            self.user_service.delete_user(pk)
            return Response({"message": "User deleted"}, status=status.HTTP_204_NO_CONTENT)

        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
