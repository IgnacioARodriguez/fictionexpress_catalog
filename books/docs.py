from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from books.serializers.book_serializer import BookSerializer
from books.serializers.book_page_serializer import BookPageSerializer

list_books_docs = extend_schema(
    summary="Lista todos los libros",
    description="Obtiene una lista paginada de libros disponibles. No incluye las páginas de los libros.",
    responses={200: BookSerializer(many=True)}
)

retrieve_book_docs = extend_schema(
    summary="Obtiene un libro por ID",
    description="Devuelve la información detallada de un libro. No incluye las páginas.",
    responses={200: BookSerializer()},
    parameters=[
        OpenApiParameter(name="id", description="ID del libro a obtener", required=True, type=int)
    ]
)

create_book_docs = extend_schema(
    summary="Crea un nuevo libro",
    description="Registra un nuevo libro con su título y autor.",
    request=BookSerializer,
    responses={201: BookSerializer()}
)

update_book_docs = extend_schema(
    summary="Actualiza un libro por su ID",
    description="""
    Permite actualizar los datos de un libro específico por su ID.
    
    - Solo los editores pueden modificar libros.
    - Los lectores solo tienen permisos de lectura.
    """,
    request=BookSerializer,
    responses={
        200: BookSerializer,
        400: {"description": "Error de validación", "content": {"application/json": {"example": {"error": "Validation failed"}}}},
        404: {"description": "Libro no encontrado", "content": {"application/json": {"example": {"error": "Book not found"}}}},
        500: {"description": "Error interno del servidor", "content": {"application/json": {"example": {"error": "Internal server error"}}}},
    },
    parameters=[
        OpenApiParameter(
            name="pk",
            description="ID del libro a actualizar",
            required=True,
            type=int,
            location=OpenApiParameter.PATH
        )
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
            description="Ejemplo de cuerpo de solicitud para actualizar un libro.",
            request_only=True
        )
    ]
)

delete_book_docs = extend_schema(
    summary="Elimina un libro",
    description="Elimina un libro de la base de datos. Solo los editores pueden realizar esta acción.",
    responses={204: None},
    parameters=[
        OpenApiParameter(name="id", description="ID del libro a eliminar", required=True, type=int)
    ]
)

list_book_pages_docs = extend_schema(
    summary="Lista las páginas de un libro",
    description="Devuelve una lista paginada de las páginas de un libro específico.",
    responses={200: BookPageSerializer(many=True)},
    parameters=[
        OpenApiParameter(name="book_id", description="ID del libro", required=True, type=int, location=OpenApiParameter.PATH),
        OpenApiParameter(name="page", description="Número de la página de paginación", required=False, type=int),
        OpenApiParameter(name="page_size", description="Cantidad de páginas por solicitud", required=False, type=int)
    ]
)


retrieve_book_page_docs = extend_schema(
    summary="Obtiene una página específica de un libro",
    description="Devuelve los detalles de una página en particular dentro de un libro.",
    responses={200: BookPageSerializer()},
    parameters=[
        OpenApiParameter(name="book_id", description="ID del libro", required=True, type=int, location=OpenApiParameter.PATH),
        OpenApiParameter(name="id", description="ID de la página dentro del libro", required=True, type=int, location=OpenApiParameter.PATH)
    ]
)


create_book_page_docs = extend_schema(
    summary="Crea una nueva página dentro de un libro",
    description="Permite a los editores agregar una nueva página a un libro específico.",
    request=BookPageSerializer,
    responses={201: BookPageSerializer},
    parameters=[
        OpenApiParameter(name="book_id", description="ID del libro al que se agregará la página", required=True, type=int, location=OpenApiParameter.PATH)
    ],
    examples=[
        OpenApiExample(name="Ejemplo de creación de página", value={
                "order": 1,
                "content": "Este es el contenido de la primera página."
            },
            description="Ejemplo de cómo enviar datos para crear una página.", request_only=True)
    ]
)