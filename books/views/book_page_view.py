from rest_framework import viewsets, status
from rest_framework.pagination import PageNumberPagination
from books.services.book_page_servicce import BookPageService
from books.serializers.book_page_serializer import BookPageSerializer
from rest_framework.response import Response
from books.docs import list_book_pages_docs


class BookPageViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = BookPageSerializer
    pagination_class = PageNumberPagination

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.page_service = BookPageService()

    @list_book_pages_docs
    def list(self, request, book_id=None):
        try:
            pages = self.page_service.get_book_pages(book_id)

            if not pages.exists():
                return Response({"message": "No hay páginas para este libro"}, status=status.HTTP_204_NO_CONTENT)

            paginator = self.pagination_class()
            paginated_pages = paginator.paginate_queryset(pages, request)

            return paginator.get_paginated_response(BookPageSerializer(paginated_pages, many=True).data)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)