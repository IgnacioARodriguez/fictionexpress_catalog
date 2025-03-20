import logging
from books.repositories.book_repository import BookRepository
from books.serializers.book_serializer import BookSerializer
from rest_framework.exceptions import NotFound, ValidationError

logger = logging.getLogger(__name__)  # Initialize logger for this module

class BookService:
    """
    Service layer for handling business logic related to books.
    """

    def __init__(self):
        """
        Initializes the BookService with a repository instance.
        """
        self.book_repository = BookRepository()

    def get_books(self):
        """
        Retrieves all books.

        :return: QuerySet containing all books.
        """
        try:
            books = self.book_repository.get_all_books()
            logger.info(f"Retrieved {len(books)} books from the database.")  # ✅ Log successful retrieval
            return books
        except Exception as e:
            logger.error(f"Error retrieving all books: {e}")  # ✅ Log unexpected errors
            return None

    def get_book_by_id(self, book_id):
        """
        Retrieves a book by its ID.

        :param book_id: The ID of the book to retrieve.
        :return: The book instance if found.
        :raises NotFound: If the book does not exist.
        """
        try:
            book = self.book_repository.get_book_by_id(book_id)
            if not book:
                logger.warning(f"Book not found: ID {book_id}")  # ✅ Log when book is not found
                raise NotFound("Book not found")
            logger.info(f"Book retrieved successfully: ID {book_id}")  # ✅ Log successful retrieval
            return book
        except Exception as e:
            logger.error(f"Error retrieving book ID {book_id}: {e}")  # ✅ Log unexpected errors
            raise

    def create_book(self, data):
        """
        Validates and creates a new book.

        :param data: A dictionary containing book details.
        :return: The created book instance.
        :raises ValidationError: If validation fails.
        """
        try:
            serializer = BookSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            book = self.book_repository.create_book(serializer.validated_data)
            print('ACA', book)
            logger.info(f"Book created successfully")  # ✅ Log successful creation
            return book
        except ValidationError as e:
            logger.warning(f"Book creation failed (validation error): {e}")  # ✅ Log validation errors
            raise
        except Exception as e:
            logger.error(f"Unexpected error creating book: {e}")  # ✅ Log unexpected errors
            raise

    def update_book(self, book_id, data):
        """
        Validates and updates an existing book.

        :param book_id: The ID of the book to update.
        :param data: A dictionary containing the fields to update.
        :return: The updated book instance.
        :raises NotFound: If the book does not exist.
        :raises ValidationError: If validation fails.
        """
        try:
            book = self.get_book_by_id(book_id)
            serializer = BookSerializer(book, data=data, partial=True)
            serializer.is_valid(raise_exception=True)
            updated_book = self.book_repository.update_book(book, serializer.validated_data)
            logger.info(f"Book updated successfully")  # ✅ Log successful update
            return updated_book
        except NotFound as e:
            logger.warning(f"Book update failed: ID {book_id} not found")  # ✅ Log book not found
            raise
        except ValidationError as e:
            logger.warning(f"Book update failed (validation error): {e}")  # ✅ Log validation errors
            raise
        except Exception as e:
            logger.error(f"Unexpected error updating book ID {book_id}: {e}")  # ✅ Log unexpected errors
            raise

    def delete_book(self, book_id):
        """
        Deletes a book by its ID.

        :param book_id: The ID of the book to delete.
        :return: None
        :raises NotFound: If the book does not exist.
        """
        try:
            book = self.book_repository.get_book_by_id(book_id)
            if not book:
                logger.warning(f"Book deletion failed: ID {book_id} not found")  # ✅ Log book not found
                raise NotFound("Book not found")

            self.book_repository.delete_book(book)
            logger.info(f"Book deleted successfully: ID {book_id}")  # ✅ Log successful deletion
        except Exception as e:
            logger.error(f"Unexpected error deleting book ID {book_id}: {e}")  # ✅ Log unexpected errors
            raise
