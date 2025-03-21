from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from books.serializers.book_serializer import BookSerializer
from books.serializers.book_page_serializer import BookPageSerializer


list_books_docs = extend_schema(
    summary="Lista todos los libros",
    description="""
    Recupera una lista paginada de libros registrados en la plataforma.

    **Notas:**
    - Solo usuarios autenticados pueden acceder.
    - No incluye las páginas del libro, solo información general.
    """,
    responses={200: BookSerializer(many=True)}
)

retrieve_book_docs = extend_schema(
    summary="Obtiene un libro por ID",
    description="""
    Recupera la información detallada de un libro en particular.

    **Notas:**
    - No incluye las páginas del libro, solo información general.
    - Disponible para todos los usuarios autenticados.
    """,
    parameters=[
        OpenApiParameter(name="id", description="ID del libro a obtener", required=True, type=int, location=OpenApiParameter.PATH)
    ],
    responses={
        200: BookSerializer(),
        404: {"description": "Libro no encontrado"},
        500: {"description": "Error interno del servidor"},
    }
)

create_book_docs = extend_schema(
    summary="Crea un nuevo libro",
    description="""
    Permite a los editores registrar un nuevo libro con su título, autor y contenido (páginas).

    **Permisos:**
    - Solo los editores pueden crear libros.
    """,
    request=BookSerializer,
    responses={
        201: BookSerializer(),
        400: {"description": "Error de validación"},
        500: {"description": "Error interno del servidor"},
    },
    examples=[
        OpenApiExample(
            name="Ejemplo de creación de libro con páginas",
            value={
                "title": "El arte de programar",
                "author": "Donald Knuth",
                "created_at": "2024-03-20T12:00:00Z",
                "updated_at": "2024-03-20T12:00:00Z",
                "pages": [
                    {
                        "page_number": 1,
                        "content": "Esta es la primera página del libro."
                    },
                    {
                        "page_number": 2,
                        "content": "Esta es la segunda página del libro."
                    }
                ]
            },
            description="Ejemplo completo con contenido paginado incluido.",
            request_only=True
        )
    ]
)

update_book_docs = extend_schema(
    summary="Actualiza un libro por ID",
    description="""
    Modifica la información de un libro específico por su ID.

    **Permisos:**
    - Solo los editores pueden modificar libros.
    - Los lectores solo tienen permisos de lectura.
    """,
    request=BookSerializer,
    responses={
        200: BookSerializer(),
        400: {"description": "Error de validación"},
        404: {"description": "Libro no encontrado"},
        500: {"description": "Error interno del servidor"},
    },
    parameters=[
        OpenApiParameter(name="pk", description="ID del libro a actualizar", required=True, type=int, location="path")
    ],
    examples=[
        OpenApiExample(
            name="Ejemplo de actualización de libro",
            value={
                "title": "Nuevo título del libro",
                "author": "Nuevo autor",
                "created_at": "2024-03-20T12:00:00Z",
                "updated_at": "2024-03-21T12:00:00Z"
            },
            description="Ejemplo de cómo enviar datos para actualizar un libro.",
            request_only=True
        )
    ]
)

delete_book_docs = extend_schema(
    summary="Elimina un libro",
    description="""
    Elimina un libro de la base de datos.

    **Permisos:**
    - Solo los editores pueden realizar esta acción.
    """,
    responses={
        204: None,
        403: {"description": "No tienes permisos para eliminar este libro"},
        404: {"description": "Libro no encontrado"},
        500: {"description": "Error interno del servidor"},
    },
    parameters=[
        OpenApiParameter(name="id", description="ID del libro a eliminar", required=True, type=int, location=OpenApiParameter.PATH)
    ]
)

list_book_pages_docs = extend_schema(
    summary="Lista las páginas de un libro",
    description="""
    Devuelve una lista paginada de las páginas de un libro específico.

    **Notas:**
    - Se puede usar paginación con `page` y `page_size`.
    - Disponible para todos los usuarios autenticados.
    """,
    responses={200: BookPageSerializer(many=True)},
    parameters=[
        OpenApiParameter(name="book_id", description="ID del libro", required=True, type=int, location=OpenApiParameter.PATH),
        OpenApiParameter(name="page", description="Número de la página de paginación", required=False, type=int),
        OpenApiParameter(name="page_size", description="Cantidad de páginas por solicitud", required=False, type=int)
    ]
)

retrieve_book_page_docs = extend_schema(exclude=True)

create_book_page_docs = extend_schema(
    summary="Crea una nueva página dentro de un libro",
    description="""
    Permite a los editores agregar una nueva página a un libro específico.

    **Permisos:**
    - Solo los editores pueden agregar páginas.
    """,
    request=BookPageSerializer,
    responses={
        201: BookPageSerializer(),
        400: {"description": "Error de validación"},
        403: {"description": "No tienes permisos para agregar una página"},
        500: {"description": "Error interno del servidor"},
    },
    parameters=[
        OpenApiParameter(name="book_id", description="ID del libro al que se agregará la página", required=True, type=int, location=OpenApiParameter.PATH)
    ],
    examples=[
        OpenApiExample(
            name="Ejemplo de creación de página",
            value={
                "page_number": 1,
                "content": "Este es el contenido de la primera página."
            },
            description="Ejemplo de cómo enviar datos para crear una página.",
            request_only=True
        )
    ]
)
