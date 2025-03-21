import logging
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from users.serializers.user_serializer import UserSerializer
from drf_spectacular.utils import extend_schema_view
from users.services.user_service import UserService
from users.models import User
from rest_framework.pagination import PageNumberPagination
from users.docs import (
    list_users_docs, get_user_by_id_docs, create_user_docs,
    update_user_docs, delete_user_docs, login_user_docs, logout_user_docs, patch_user_docs
)

logger = logging.getLogger(__name__)  # Initialize logger for this module

@extend_schema_view(
    partial_update=patch_user_docs  # Oculta `PATCH` en Swagger
)
class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing users, including authentication, retrieval, updating, and deletion.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    user_service = UserService()

    def get_permissions(self):
        """
        Assigns different permissions based on the action.

        - `AllowAny` for `create` (signup) and `login`.
        - `IsAuthenticated` for all other actions.

        :return: List of permissions for the requested action.
        """
        if self.action in ["create", "login"]:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    @login_user_docs
    @action(detail=False, methods=["post"])
    def login(self, request):
        """
        Authenticates a user and returns access and refresh tokens.

        :param request: The HTTP request containing user credentials.
        :return: JSON with `access` and `refresh` tokens.
        :raises HTTP_400_BAD_REQUEST: If authentication fails.
        """
        try:
            email = request.data.get("email")
            logger.info(f"User login attempt: {email}")
            token_data = self.user_service.authenticate_user(
                email=email, password=request.data.get("password")
            )
            logger.info(f"User logged in successfully: {email}")
            return Response(token_data, status=status.HTTP_200_OK)

        except Exception as e:
            logger.warning(f"User login failed: {email} - {e}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @create_user_docs
    def create(self, request):
        """
        Registers a new user.

        :param request: The HTTP request containing user registration data.
        :return: JSON with user details.
        :raises HTTP_400_BAD_REQUEST: If validation fails.
        """
        try:
            email = request.data.get("email")
            logger.info(f"User signup attempt: {email}")
            serializer = UserSerializer(data=request.data)

            if serializer.is_valid():
                user_data = self.user_service.create_user(serializer.validated_data)
                logger.info(f"User registered successfully: {user_data['email']}")
                return Response(user_data, status=status.HTTP_201_CREATED)

            logger.warning(f"User signup failed (invalid data): {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.error(f"Unexpected error during signup: {e}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @logout_user_docs
    @action(detail=False, methods=["post"], permission_classes=[permissions.IsAuthenticated])
    def logout(self, request):
        """
        Logs out the user by blacklisting the provided refresh token.

        :param request: The HTTP request containing the refresh token.
        :return: JSON with logout confirmation message.
        :raises HTTP_400_BAD_REQUEST: If logout fails.
        """
        try:
            logger.info(f"User logout attempt: {request.user.email}")
            refresh_token = request.data.get("refresh")
            self.user_service.logout_user(refresh_token)
            logger.info(f"User logged out successfully: {request.user.email}")
            return Response({"message": "Logged out"}, status=status.HTTP_200_OK)

        except Exception as e:
            logger.warning(f"User logout failed: {request.user.email} - {e}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @list_users_docs
    def list(self, request):
        """
        Retrieves a paginated list of all users.

        :param request: The HTTP request object.
        :return: Paginated JSON response with user details.
        :raises HTTP_403_FORBIDDEN: If a non-admin user tries to access.
        :raises HTTP_500_INTERNAL_SERVER_ERROR: If an unexpected server error occurs.
        """
        if not request.user.is_staff:
            logger.warning(f"Unauthorized user list attempt by {request.user.email}")
            return Response({"error": "You do not have permission"}, status=status.HTTP_403_FORBIDDEN)

        try:
            users = self.user_service.get_all_users()
            if not users.exists():
                logger.info("User list requested - No users found")
                return Response({"message": "No users available"}, status=status.HTTP_204_NO_CONTENT)

            paginator = PageNumberPagination()
            paginated_users = paginator.paginate_queryset(users, request)
            logger.info(f"User list retrieved successfully ({users.count()} users)")
            return paginator.get_paginated_response(UserSerializer(paginated_users, many=True).data)

        except Exception as e:
            logger.error(f"Unexpected error retrieving user list: {e}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @get_user_by_id_docs
    def retrieve(self, request, pk=None):
        """
        Retrieves a user by their ID.

        :param request: The HTTP request object.
        :param pk: The ID of the user to retrieve.
        :return: JSON with user details.
        :raises HTTP_404_NOT_FOUND: If the user does not exist.
        :raises HTTP_500_INTERNAL_SERVER_ERROR: If an unexpected server error occurs.
        """
        try:
            user = self.user_service.get_user_by_id(pk)
            if not request.user.is_staff and request.user.id != user.id:
                logger.warning(f"Unauthorized user retrieval attempt by {request.user.email}")
                return Response({"error": "You do not have permission"}, status=status.HTTP_403_FORBIDDEN)

            logger.info(f"User retrieved successfully: {user.email}")
            return Response(UserSerializer(user).data)

        except ValueError as e:
            logger.warning(f"User not found: ID {pk}")
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            logger.error(f"Unexpected error retrieving user ID {pk}: {e}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    @update_user_docs
    def update(self, request, pk=None):
        """
        Updates a user's details (Only the account owner).

        :param request: The HTTP request object.
        :param pk: The ID of the user to update.
        :return: JSON with updated user details.
        :raises HTTP_404_NOT_FOUND: If the user does not exist.
        :raises HTTP_500_INTERNAL_SERVER_ERROR: If an unexpected server error occurs
        """
        if request.user.id != int(pk):
            logger.warning(f"Unauthorized user update attempt by {request.user.email}")
            return Response({"error": "You do not have permission"}, status=status.HTTP_403_FORBIDDEN)

        try:
            user = self.user_service.update_user(pk, request.data)
            logger.info(f"User updated successfully: {user.email}")
            return Response(UserSerializer(user).data)

        except ValueError as e:
            logger.warning(f"User update failed: User ID {pk} not found")
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            logger.error(f"Unexpected error updating user ID {pk}: {e}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @delete_user_docs
    def destroy(self, request, pk=None):
        """
        Deletes a user.

        :param request: The HTTP request object.
        :param pk: The ID of the user to delete.
        :return: JSON confirmation message.
        :raises HTTP_404_NOT_FOUND: If the user does not exist.
        :raises HTTP_500_INTERNAL_SERVER_ERROR: If an unexpected server error occurs.
        """
        if not request.user.is_staff:
            logger.warning(f"Unauthorized user deletion attempt by {request.user.email}")
            return Response({"error": "You do not have permission"}, status=status.HTTP_403_FORBIDDEN)

        try:
            self.user_service.delete_user(pk)
            logger.info(f"User deleted successfully: ID {pk}")
            return Response({"message": "User deleted"}, status=status.HTTP_204_NO_CONTENT)

        except ValueError as e:
            logger.warning(f"User deletion failed: User ID {pk} not found")
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
