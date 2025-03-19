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
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    user_service = UserService()

    @login_user_docs
    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def login(self, request):
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
        try:
            refresh_token = request.data.get('refresh')
            self.user_service.logout_user(refresh_token)
            return Response({"message": "Logged out"}, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


    @list_users_docs
    def list(self, request):
        if not request.user.is_staff:
            return Response({"error": "No tienes permisos"}, status=status.HTTP_403_FORBIDDEN)

        try:
            users = self.user_service.get_all_users()

            if not users.exists():
                return Response({"message": "No hay usuarios disponibles"}, status=status.HTTP_204_NO_CONTENT)

            paginator = PageNumberPagination()
            paginated_users = paginator.paginate_queryset(users, request)

            return paginator.get_paginated_response(UserSerializer(paginated_users, many=True).data)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

    @get_user_by_id_docs
    def retrieve(self, request, pk=None):
        try:
            user = self.user_service.get_user_by_id(pk)
            if not request.user.is_staff and request.user.id != user.id:
                return Response({"error": "No tienes permisos"}, status=status.HTTP_403_FORBIDDEN)

            else:
                return Response(UserSerializer(user).data)

        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

    @update_user_docs
    def update(self, request, pk=None):
        if request.user.id != int(pk):
            return Response({"error": "No tienes permisos"}, status=status.HTTP_403_FORBIDDEN)
        try:
            user = self.user_service.update_user(pk, request.data)
            return Response(UserSerializer(user).data)

        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

    @delete_user_docs
    def destroy(self, request, pk=None):
        if not request.user.is_staff:
            return Response({"error": "No tienes permisos"}, status=status.HTTP_403_FORBIDDEN)
        try:
            self.user_service.delete_user(pk)
            return Response({"message": "Usuario eliminado"}, status=status.HTTP_204_NO_CONTENT)

        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
