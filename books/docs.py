from drf_spectacular.utils import extend_schema, OpenApiParameter
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
        OpenApiParameter(name="book_id", description="ID del libro", required=True, type=int),
        OpenApiParameter(name="page", description="Número de la página de paginación", required=False, type=int),
        OpenApiParameter(name="page_size", description="Cantidad de páginas por solicitud", required=False, type=int)
    ]
)
