from books.models import Book

class BookRepository:
    @staticmethod
    def get_all_books():
        return Book.objects.all()

    @staticmethod
    def get_book_by_id(book_id):
        return Book.objects.filter(id=book_id).first()

    @staticmethod
    def create_book(data):
        return Book.objects.create(**data)

    @staticmethod
    def delete_book(book):
        book.delete()