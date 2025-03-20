from books.repositories.book_page_repository import BookPageRepository


class BookPageService:
    def __init__(self):
        self.page_repository = BookPageRepository()

    def get_book_pages(self, book_id):
        pages = self.page_repository.get_pages_by_book(book_id)
        return pages