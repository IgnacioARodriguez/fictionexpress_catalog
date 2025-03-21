import logging
from books.models import Book, BookPage

logger = logging.getLogger(__name__)  

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
        try:
            books = Book.objects.all()
            logger.info(f"Retrieved {books.count()} books from the database.")
            return books
        except Exception as e:
            logger.error(f"Error retrieving all books: {e}")  
            return None

    @staticmethod
    def get_book_by_id(book_id):
        """
        Retrieves a book by its ID.

        :param book_id: The ID of the book to retrieve.
        :return: The book object if found, otherwise None.
        """
        try:
            book = Book.objects.filter(id=book_id).first()
            if book:
                logger.info(f"Book retrieved successfully: ID {book_id}")  
            else:
                logger.warning(f"Book not found: ID {book_id}") 
            return book
        except Exception as e:
            logger.error(f"Error retrieving book ID {book_id}: {e}")  
            return None

    @staticmethod
    def create_book(data):
        """
        Creates a new book along with its associated pages.

        :param data: A dictionary containing book details, including optional pages.
        :return: The created book instance.
        """
        try:
            pages_data = data.pop("pages", [])
            book = Book.objects.create(**data)
            logger.info(f"Book created successfully: ID {book.id}, Title: {book.title}") 

            for page_data in pages_data:
                BookPage.objects.create(book=book, **page_data)
            logger.info(f"{len(pages_data)} pages added to book ID {book.id}") 

            return book
        except Exception as e:
            logger.error(f"Error creating book: {e}") 
            return None
    
    @staticmethod
    def update_book(book, data):
        """
        Updates an existing book with new data.

        :param book: The book instance to update.
        :param data: A dictionary containing the fields to update.
        :return: The updated book instance.
        """
        try:
            for key, value in data.items():
                setattr(book, key, value) 
            book.save()
            logger.info(f"Book updated successfully: ID {book.id}, Title: {book.title}")  
            return book
        except Exception as e:
            logger.error(f"Error updating book ID {book.id}: {e}")  
            return None

    @staticmethod
    def delete_book(book):
        """
        Deletes a book from the database.

        :param book: The book instance to delete.
        """
        try:
            book_id = book.id 
            title = book.title
            book.delete()
            logger.info(f"Book deleted successfully: ID {book_id}, Title: {title}")  
        except Exception as e:
            logger.error(f"Error deleting book ID {book.id}: {e}")  
