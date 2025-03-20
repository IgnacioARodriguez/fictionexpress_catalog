from books.repositories.book_repository import BookRepository
from books.serializers.book_serializer import BookSerializer
from rest_framework.exceptions import NotFound


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
        return self.book_repository.get_all_books()

    def get_book_by_id(self, book_id):
        """
        Retrieves a book by its ID.

        :param book_id: The ID of the book to retrieve.
        :return: The book instance if found.
        :raises NotFound: If the book does not exist.
        """
        book = self.book_repository.get_book_by_id(book_id)
        if not book:
            raise NotFound("Book not found")
        return book

    def create_book(self, data):
        """
        Validates and creates a new book.

        :param data: A dictionary containing book details.
        :return: The created book instance.
        :raises ValidationError: If validation fails.
        """
        serializer = BookSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        return self.book_repository.create_book(serializer.validated_data)
    
    def update_book(self, book_id, data):
        """
        Validates and updates an existing book.

        :param book_id: The ID of the book to update.
        :param data: A dictionary containing the fields to update.
        :return: The updated book instance.
        :raises NotFound: If the book does not exist.
        :raises ValidationError: If validation fails.
        """
        book = self.get_book_by_id(book_id)
        serializer = BookSerializer(book, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        return self.book_repository.update_book(book, serializer.validated_data)

    def delete_book(self, book_id):
        """
        Deletes a book by its ID.

        :param book_id: The ID of the book to delete.
        :return: None
        :raises NotFound: If the book does not exist.
        """
        book = self.book_repository.get_book_by_id(book_id)
        if not book:
            raise NotFound("Book not found")
        self.book_repository.delete_book(book)
