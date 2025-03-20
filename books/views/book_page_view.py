from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import NotFound
from books.services.book_page_servicce import BookPageService
from books.serializers.book_page_serializer import BookPageSerializer
from books.docs import list_book_pages_docs

class BookPagePagination(PageNumberPagination):
    """
    Pagination settings for book pages.

    - `page_size`: Number of pages per request (default: 10).
    - `page_size_query_param`: Allows dynamic page size via query parameters.
    - `max_page_size`: Maximum number of pages per request.
    """
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100

class BookPageViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for retrieving book pages with pagination.

    This endpoint allows users to list the pages of a specific book
    while applying pagination settings to optimize response size.
    """

    serializer_class = BookPageSerializer
    pagination_class = BookPagePagination

    def __init__(self, **kwargs):
        """
        Initializes the BookPageViewSet with a BookPageService instance.
        """
        super().__init__(**kwargs)
        self.page_service = BookPageService()

    @list_book_pages_docs
    def list(self, request, book_id=None):
        """
        Retrieves the paginated list of pages for a specific book.

        :param request: The HTTP request object.
        :param book_id: The ID of the book whose pages are being retrieved.
        :return: A paginated response containing the book's pages.
        :raises NotFound: If no pages are found for the specified book.
        :raises Exception: If an unexpected server error occurs.
        """
        try:
            pages = self.page_service.get_book_pages(book_id)

            if not pages.exists():
                raise NotFound("No pages available for this book")

            paginator = self.pagination_class()
            paginated_pages = paginator.paginate_queryset(pages, request)

            return paginator.get_paginated_response(BookPageSerializer(paginated_pages, many=True).data)

        except NotFound as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": "Internal server error", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
