from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status
from users.serializers.user_serializer import UserSerializer

list_users_docs = extend_schema(
    summary="Lista todos los usuarios",
    description="Devuelve una lista paginada de usuarios. Solo accesible por administradores.",
    responses={200: UserSerializer(many=True)},
)

get_user_by_id_docs = extend_schema(
    summary="Obtiene los detalles de un usuario",
    description="Devuelve la información de un usuario dado su ID. Solo accesible por administradores y el mismo usuario.",
    parameters=[
        OpenApiParameter("id", description="ID del usuario", type=int),
    ],
    responses={200: UserSerializer()},
)

create_user_docs = extend_schema(
    summary="Crea un nuevo usuario",
    description="Registra un nuevo usuario con los datos proporcionados.",
    request=UserSerializer,
    responses={
        201: UserSerializer,
        400: {"description": "Error en los datos proporcionados"},
    },
)

update_user_docs = extend_schema(
    summary="Actualiza un usuario",
    description="Modifica la información de un usuario existente. Solo accesible por administradores y el mismo usuario.",
    parameters=[
        OpenApiParameter("id", description="ID del usuario", type=int),
    ],
    request=UserSerializer,
    responses={
        200: UserSerializer,
        400: {"description": "Error en los datos proporcionados"},
        403: {"description": "No tienes permisos para modificar este usuario"},
        404: {"description": "Usuario no encontrado"},
    },
)

delete_user_docs = extend_schema(
    summary="Elimina un usuario",
    description="Elimina un usuario por su ID. Solo accesible por administradores.",
    parameters=[
        OpenApiParameter("id", description="ID del usuario", type=int),
    ],
    responses={
        204: {"description": "Usuario eliminado correctamente"},
        403: {"description": "No tienes permisos para eliminar este usuario"},
        404: {"description": "Usuario no encontrado"},
    },
)

login_user_docs = extend_schema(
    summary="Autenticación de usuario",
    description="Inicia sesión y obtiene un token JWT.",
    request={
        "application/json": {
            "example": {
                "email": "user@example.com",
                "password": "password123",
            }
        }
    },
    responses={
        200: {
            "application/json": {
                "example": {
                    "access": "jwt_access_token",
                    "refresh": "jwt_refresh_token",
                }
            }
        },
        400: {"description": "Credenciales inválidas"},
    },
)

logout_user_docs = extend_schema(
    summary="Cierra sesión",
    description="Revoca el token de refresco y cierra sesión del usuario.",
    request={
        "application/json": {
            "example": {
                "refresh": "jwt_refresh_token",
            }
        }
    },
    responses={
        200: {"description": "Sesión cerrada correctamente"},
        400: {"description": "Token inválido o expirado"},
    },
)
