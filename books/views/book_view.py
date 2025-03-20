from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound, ValidationError
from books.services.book_service import BookService
from books.serializers.book_serializer import BookSerializer
from books.permissions.book_permissions import IsEditorOrReadOnly
from books.docs import (  
    list_books_docs, retrieve_book_docs, create_book_docs, delete_book_docs
)

class BookPagination(PageNumberPagination):
    """Configuración de paginación para los libros."""
    page_size = 5
    page_size_query_param = "page_size"
    max_page_size = 100

class BookViewSet(viewsets.ViewSet):
    """
    ViewSet para gestionar libros con permisos RBAC y paginación.
    """

    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated, IsEditorOrReadOnly]
    pagination_class = BookPagination

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.book_service = BookService()

    @list_books_docs
    def list(self, request):
        """
        Lista los libros paginados.
        """
        try:
            books = self.book_service.get_books()

            if not books.exists():
                return Response({"message": "No hay libros disponibles"}, status=status.HTTP_204_NO_CONTENT)

            paginator = self.pagination_class()
            paginated_books = paginator.paginate_queryset(books, request)

            return paginator.get_paginated_response(BookSerializer(paginated_books, many=True).data)

        except Exception as e:
            return Response({"error": "Error interno del servidor", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @retrieve_book_docs
    def retrieve(self, request, pk=None):
        """
        Obtiene un libro por ID.
        """
        try:
            book = self.book_service.get_book_by_id(pk)
            return Response(BookSerializer(book).data)
        except NotFound:
            return Response({"error": "Libro no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        except Exception:
            return Response({"error": "Error interno del servidor"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @create_book_docs
    def create(self, request):
        """
        Crea un nuevo libro.
        """
        try:
            book = self.book_service.create_book(request.data)
            return Response(BookSerializer(book).data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({"error": e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response({"error": "Error interno del servidor"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, pk=None):
        """
        Actualiza un libro por ID.
        """
        try:
            book = self.book_service.update_book(pk, request.data)
            return Response(BookSerializer(book).data, status=status.HTTP_200_OK)
        except NotFound:
            return Response({"error": "Libro no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        except ValidationError as e:
            return Response({"error": e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response({"error": "Error interno del servidor"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @delete_book_docs
    def destroy(self, request, pk=None):
        """
        Elimina un libro.
        """
        try:
            self.book_service.delete_book(pk)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except NotFound:
            return Response({"error": "Libro no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        except Exception:
            return Response({"error": "Error interno del servidor"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
