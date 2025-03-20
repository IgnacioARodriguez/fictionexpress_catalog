from books.models import BookPage


class BookPageRepository:
    @staticmethod
    def get_pages_by_book(book_id):
        return BookPage.objects.filter(book_id=book_id).order_by("page_number")