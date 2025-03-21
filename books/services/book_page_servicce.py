import logging
from books.repositories.book_page_repository import BookPageRepository

logger = logging.getLogger(__name__) 

class BookPageService:
    """
    Service layer for handling business logic related to book pages.
    """

    def __init__(self):
        """
        Initializes the BookPageService with a repository instance.
        """
        self.page_repository = BookPageRepository()

    def get_book_pages(self, book_id):
        """
        Retrieves all pages for a specific book.

        :param book_id: The ID of the book whose pages are being retrieved.
        :return: QuerySet containing the book's pages.
        """
        try:
            pages = self.page_repository.get_pages_by_book(book_id)
            if pages and pages.exists():
                logger.info(f"Retrieved {pages.count()} pages for book ID {book_id}") 
            else:
                logger.warning(f"No pages found for book ID {book_id}")  
            return pages
        except Exception as e:
            logger.error(f"Error retrieving pages for book ID {book_id}: {e}") 
            return None
        

    def get_book_page(self, book_id, page_id):
        """
        Fetch a specific page of a book.

        :param book_id: The ID of the book containing the page.
        :param page_id: The ID of the page to retrieve.
        :return: The requested page object.
        """
        try:
            page = self.page_repository.get_page_by_id(book_id, page_id)
            if page:
                logger.info(f"Retrieved page {page_id} for book ID {book_id}")
            else:
                logger.warning(f"Page {page_id} not found for book ID {book_id}")
            return page
        except Exception as e:
            logger.error(f"Error retrieving page {page_id} for book ID {book_id}: {e}")
            return None
        

    def get_page_by_id(self, book_id, page_id):
        """
        Fetch a specific page of a book.

        :param book_id: The ID of the book containing the page.
        :param page_id: The ID of the page to retrieve.
        :return: The requested page object.
        """
        try:
            page = self.page_repository.get_page_by_id(book_id, page_id)
            if page:
                logger.info(f"Retrieved page {page_id} for book ID {book_id}")
            else:
                logger.warning(f"Page {page_id} not found for book ID {book_id}")
            return page
        except Exception as e:
            logger.error(f"Error retrieving page {page_id} for book ID {book_id}: {e}")
            return None
