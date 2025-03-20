import logging
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

logger = logging.getLogger(__name__)  # Initialize logger for this module

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
        """
        try:
            logger.info(f"User login attempt: {request.data.get('email')}")
            token_data = self.user_service.authenticate_user(
                email=request.data.get('email'), password=request.data.get('password')
            )
            logger.info(f"User logged in successfully: {request.data.get('email')}")
            return Response(token_data, status=status.HTTP_200_OK)

        except Exception as e:
            logger.warning(f"User login failed: {request.data.get('email')} - {e}")
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @create_user_docs
    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def signup(self, request):
        """
        Registers a new user.
        """
        try:
            logger.info(f"User signup attempt: {request.data.get('email')}")
            serializer = UserSerializer(data=request.data)

            if serializer.is_valid():
                user_data = self.user_service.create_user(serializer.validated_data)
                logger.info(f"User registered successfully: {user_data['email']}")
                return Response(user_data, status=status.HTTP_201_CREATED)

            else:
                logger.warning(f"User signup failed (invalid data): {serializer.errors}")
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.error(f"Unexpected error during signup: {e}")
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @logout_user_docs
    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def logout(self, request):
        """
        Logs out the user by blacklisting the provided refresh token.
        """
        try:
            logger.info(f"User logout attempt: {request.user.email}")
            refresh_token = request.data.get('refresh')
            self.user_service.logout_user(refresh_token)
            logger.info(f"User logged out successfully: {request.user.email}")
            return Response({"message": "Logged out"}, status=status.HTTP_200_OK)

        except Exception as e:
            logger.warning(f"User logout failed: {request.user.email} - {e}")
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @list_users_docs
    def list(self, request):
        """
        Lists all users (Admin only).
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
        Retrieves a user by ID (Admins or the user themselves).
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
        Deletes a user (Admin only).
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

        except Exception as e:
            logger.error(f"Unexpected error deleting user ID {pk}: {e}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
