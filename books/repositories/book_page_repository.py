import logging
from books.models import BookPage

logger = logging.getLogger(__name__) 

class BookPageRepository:
    """
    Repository class for handling database operations related to book pages.
    """

    @staticmethod
    def get_pages_by_book(book_id):
        """
        Retrieves all pages of a specific book, ordered by page number.

        :param book_id: The ID of the book whose pages are being retrieved.
        :return: QuerySet containing the book's pages.
        """
        try:
            pages = BookPage.objects.filter(book_id=book_id).order_by("page_number")
            if pages.exists():
                logger.info(f"Retrieved {pages.count()} pages for book ID {book_id}")
            else:
                logger.warning(f"No pages found for book ID {book_id}")
            return pages
        except Exception as e:
            logger.error(f"Error retrieving pages for book ID {book_id}: {e}") 
            return None
