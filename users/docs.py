from drf_spectacular.utils import extend_schema, OpenApiParameter
from users.serializers.user_serializer import UserSerializer
from rest_framework import serializers
from drf_spectacular.utils import OpenApiExample


class LoginRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

class LogoutRequestSerializer(serializers.Serializer):
    refresh = serializers.CharField()


list_users_docs = extend_schema(
    summary="Lista todos los usuarios",
    description="""
    Recupera una lista paginada de usuarios registrados en la plataforma.
    
    **Permisos:**
    - Solo accesible por administradores.
    """,
    responses={200: UserSerializer(many=True)},
)

get_user_by_id_docs = extend_schema(
    summary="Obtiene los detalles de un usuario",
    description="""
    Recupera la información de un usuario específico dado su ID.

    **Permisos:**
    - Accesible por administradores.
    - Un usuario puede acceder a su propia información.
    """,
    parameters=[
        OpenApiParameter("id", description="ID del usuario", required=True, type=int, location="path"),
    ],
    responses={
        200: UserSerializer(),
        403: {"description": "No tienes permisos para acceder a este usuario"},
        404: {"description": "Usuario no encontrado"},
    },
)

create_user_docs = extend_schema(
    summary="Crea un nuevo usuario",
    description="""
    Registra un nuevo usuario con los datos proporcionados.

    **Permisos:**
    - No requiere autenticación.
    """,
    request=UserSerializer,
    responses={
        201: UserSerializer,
        400: {"description": "Error en los datos proporcionados"},
    },
    examples=[
        OpenApiExample(
            name="Ejemplo de creación de usuario",
            value={
                "email": "newuser@example.com",
                "password": "securepassword",
                "username": "newuser",
                "role": "reader"
            },
            request_only=True
        )
    ]
)

update_user_docs = extend_schema(
    summary="Actualiza un usuario",
    description="""
    Modifica la información de un usuario existente.

    **Permisos:**
    - Un usuario puede actualizar solo su propia cuenta.
    - Administradores pueden modificar cualquier usuario.
    """,
    parameters=[
        OpenApiParameter("id", description="ID del usuario", required=True, type=int, location="path"),
    ],
    request=UserSerializer,
    responses={
        200: UserSerializer,
        400: {"description": "Error en los datos proporcionados"},
        403: {"description": "No tienes permisos para modificar este usuario"},
        404: {"description": "Usuario no encontrado"},
    },
    examples=[
        OpenApiExample(
            name="Ejemplo de actualización de usuario",
            value={
                "email": "updateduser@example.com",
                "username": "updateduser",
                "role": "editor"
            },
            request_only=True
        )
    ]
)

delete_user_docs = extend_schema(
    summary="Elimina un usuario",
    description="""
    Elimina un usuario de la plataforma.

    **Permisos:**
    - Solo administradores pueden eliminar usuarios.
    """,
    parameters=[
        OpenApiParameter("id", description="ID del usuario", required=True, type=int, location="path"),
    ],
    responses={
        204: {"description": "Usuario eliminado correctamente"},
        403: {"description": "No tienes permisos para eliminar este usuario"},
        404: {"description": "Usuario no encontrado"},
    },
)

login_user_docs = extend_schema(
    summary="Autenticación de usuario",
    description="""
    Inicia sesión con las credenciales del usuario y obtiene un token JWT.
    
    **Permisos:**
    - No requiere autenticación.
    """,
    request=LoginRequestSerializer,
    responses={
        200: OpenApiExample(
            name="Token de respuesta",
            value={
                "access": "jwt_access_token",
                "refresh": "jwt_refresh_token"
            },
            response_only=True
        ),
        400: {"description": "Credenciales inválidas"},
    },
    examples=[
        OpenApiExample(
            name="Ejemplo de login",
            value={
                "email": "user@example.com",
                "password": "password123"
            },
            request_only=True
        )
    ]
)

logout_user_docs = extend_schema(
    summary="Cierra sesión",
    description="""
    Revoca el token de refresco y cierra sesión del usuario.

    **Permisos:**
    - Requiere autenticación.
    """,
    request=LogoutRequestSerializer,
    responses={
        200: {"description": "Sesión cerrada correctamente"},
        400: {"description": "Token inválido o expirado"},
    },
    examples=[
        OpenApiExample(
            name="Ejemplo de logout",
            value={
                "refresh": "jwt_refresh_token"
            },
            request_only=True
        )
    ]
)

patch_user_docs = extend_schema(exclude=True)
