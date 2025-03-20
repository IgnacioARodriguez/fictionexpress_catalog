from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import NotFound
from books.services.book_page_servicce import BookPageService
from books.serializers.book_page_serializer import BookPageSerializer
from books.docs import list_book_pages_docs

class BookPagePagination(PageNumberPagination):
    """Configuración de paginación para las páginas de los libros."""
    page_size = 10  # 🔹 Número de páginas por solicitud
    page_size_query_param = "page_size"
    max_page_size = 100

class BookPageViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet para obtener páginas de un libro con paginación.
    """

    serializer_class = BookPageSerializer
    pagination_class = BookPagePagination

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.page_service = BookPageService()

    @list_book_pages_docs
    def list(self, request, book_id=None):
        """
        Lista las páginas de un libro con paginación.
        """
        try:
            pages = self.page_service.get_book_pages(book_id)

            if not pages.exists():
                raise NotFound("No hay páginas para este libro")  # 🔹 Mejor manejo del error

            paginator = self.pagination_class()
            paginated_pages = paginator.paginate_queryset(pages, request)

            return paginator.get_paginated_response(BookPageSerializer(paginated_pages, many=True).data)

        except NotFound as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception:
            return Response({"error": "Error interno del servidor"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
