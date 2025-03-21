import logging
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound, ValidationError
from books.services.book_service import BookService
from books.serializers.book_serializer import BookSerializer
from books.permissions.book_permissions import IsEditorOrReadOnly
from books.docs import (  
    list_books_docs, retrieve_book_docs, create_book_docs, delete_book_docs, update_book_docs
)

logger = logging.getLogger(__name__)

class BookPagination(PageNumberPagination):
    """
    Pagination settings for books.

    - `page_size`: Number of books per request (default: 5).
    - `page_size_query_param`: Allows dynamic page size via query parameters.
    - `max_page_size`: Maximum number of books per request.
    """
    page_size = 5
    page_size_query_param = "page_size"
    max_page_size = 100

class BookViewSet(viewsets.ViewSet):
    """
    ViewSet for managing books with RBAC (Role-Based Access Control) and pagination.

    Permissions:
    - Authenticated users can read books.
    - Only editors can create, update, and delete books.
    """

    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated, IsEditorOrReadOnly]
    pagination_class = BookPagination

    def __init__(self, **kwargs):
        """
        Initializes the BookViewSet with a BookService instance.
        """
        super().__init__(**kwargs)
        self.book_service = BookService()

    @list_books_docs
    def list(self, request):
        """
        Retrieves a paginated list of books.

        :param request: The HTTP request object.
        :return: A paginated response containing the list of books.
        :raises Exception: If an unexpected server error occurs.
        """
        try:
            logger.info("Fetching list of books")
            books = self.book_service.get_books()

            if not books.exists():
                logger.warning("No books found in the database")
                return Response({"message": "No books available"}, status=status.HTTP_204_NO_CONTENT)

            paginator = self.pagination_class()
            paginated_books = paginator.paginate_queryset(books, request)
            logger.info(f"Retrieved {books.count()} books")

            return paginator.get_paginated_response(BookSerializer(paginated_books, many=True).data)

        except Exception as e:
            logger.error(f"Unexpected error fetching books: {e}")
            return Response({"error": "Internal server error", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @retrieve_book_docs
    def retrieve(self, request, pk=None):
        """
        Retrieves a book by its ID.

        :param request: The HTTP request object.
        :param pk: The ID of the book to retrieve.
        :return: The book details in JSON format.
        :raises NotFound: If the book does not exist.
        :raises Exception: If an unexpected server error occurs.
        """
        try:
            logger.info(f"Fetching book with ID {pk}")
            book = self.book_service.get_book_by_id(pk)
            logger.info(f"Book retrieved successfully: ID {pk}")
            return Response(BookSerializer(book).data)
        except NotFound:
            logger.warning(f"Book not found: ID {pk}")
            return Response({"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Unexpected error retrieving book ID {pk}: {e}")
            return Response({"error": "Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @create_book_docs
    def create(self, request):
        """
        Creates a new book.

        :param request: The HTTP request containing book data.
        :return: The created book details in JSON format.
        :raises ValidationError: If validation fails.
        :raises Exception: If an unexpected server error occurs.
        """
        try:
            logger.info(f"Creating book with data: {request.data}")
            book = self.book_service.create_book(request.data)
            logger.info(f"Book created successfully: ID {book.id}, Title: {book.title}")
            return Response(BookSerializer(book).data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            logger.warning(f"Book creation failed (validation error): {e}")
            return Response({"error": e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Unexpected error creating book: {e}")
            return Response({"error": "Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @update_book_docs
    def update(self, request, pk=None):
        """
        Updates a book by its ID.

        :param request: The HTTP request containing updated book data.
        :param pk: The ID of the book to update.
        :return: The updated book details in JSON format.
        :raises NotFound: If the book does not exist.
        :raises ValidationError: If validation fails.
        :raises Exception: If an unexpected server error occurs.
        """
        try:
            logger.info(f"Updating book with ID {pk}")
            book = self.book_service.update_book(pk, request.data)
            logger.info(f"Book updated successfully: ID {book.id}, Title: {book.title}")
            return Response(BookSerializer(book).data, status=status.HTTP_200_OK)
        except NotFound:
            logger.warning(f"Book update failed: ID {pk} not found")
            return Response({"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND)
        except ValidationError as e:
            logger.warning(f"Book update failed (validation error): {e}")
            return Response({"error": e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Unexpected error updating book ID {pk}: {e}")
            return Response({"error": "Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @delete_book_docs
    def destroy(self, request, pk=None):
        """
        Deletes a book by its ID.

        :param request: The HTTP request.
        :param pk: The ID of the book to delete.
        :return: A JSON response confirming deletion.
        :raises NotFound: If the book does not exist.
        :raises Exception: If an unexpected server error occurs.
        """
        try:
            logger.info(f"Deleting book with ID {pk}")
            self.book_service.delete_book(pk)
            logger.info(f"Book deleted successfully: ID {pk}")
            return Response(status=status.HTTP_204_NO_CONTENT)
        except NotFound:
            logger.warning(f"Book deletion failed: ID {pk} not found")
            return Response({"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Unexpected error deleting book ID {pk}: {e}")
            return Response({"error": "Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
