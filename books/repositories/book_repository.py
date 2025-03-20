from books.models import Book
from books.models import BookPage

class BookRepository:
    @staticmethod
    def get_all_books():
        return Book.objects.all()

    @staticmethod
    def get_book_by_id(book_id):
        return Book.objects.filter(id=book_id).first()

    @staticmethod
    def create_book(data):
        pages_data = data.pop("pages", []) 
        book = Book.objects.create(**data) 

        for page_data in pages_data:
            BookPage.objects.create(book=book, **page_data)

        return book
    
    @staticmethod
    def update_book(book, data):
        for key, value in data.items():
            setattr(book, key, value) 
        book.save()
        return book

    @staticmethod
    def delete_book(book):
        book.delete()