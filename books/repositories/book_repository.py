from books.models import Book
from books.models import BookPage

class BookRepository:
    """
    Repository class for handling database operations related to books.
    """

    @staticmethod
    def get_all_books():
        """
        Retrieves all books from the database.

        :return: QuerySet containing all books.
        """
        return Book.objects.all()

    @staticmethod
    def get_book_by_id(book_id):
        """
        Retrieves a book by its ID.

        :param book_id: The ID of the book to retrieve.
        :return: The book object if found, otherwise None.
        """
        return Book.objects.filter(id=book_id).first()

    @staticmethod
    def create_book(data):
        """
        Creates a new book along with its associated pages.

        :param data: A dictionary containing book details, including optional pages.
        :return: The created book instance.
        """
        pages_data = data.pop("pages", [])  # Extract pages data if present
        book = Book.objects.create(**data)  # Create book instance

        for page_data in pages_data:
            BookPage.objects.create(book=book, **page_data)  # Create book pages

        return book
    
    @staticmethod
    def update_book(book, data):
        """
        Updates an existing book with new data.

        :param book: The book instance to update.
        :param data: A dictionary containing the fields to update.
        :return: The updated book instance.
        """
        for key, value in data.items():
            setattr(book, key, value)  # Dynamically update book attributes
        book.save()
        return book

    @staticmethod
    def delete_book(book):
        """
        Deletes a book from the database.

        :param book: The book instance to delete.
        """
        book.delete()
