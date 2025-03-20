from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from books.services.book_page_servicce import BookPageService
from books.serializers.book_serializer import BookPageSerializer


class BookPageViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = BookPageSerializer
    pagination_class = PageNumberPagination

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.page_service = BookPageService()

    def get_queryset(self):
        book_id = self.kwargs.get("book_id")
        try:
            return self.page_service.get_book_pages(book_id)
        except ValueError:
            return []