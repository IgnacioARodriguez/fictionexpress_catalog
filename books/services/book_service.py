from books.repositories.book_repository import BookRepository

class BookService:
    def __init__(self):
        self.book_repository = BookRepository()

    def get_books(self):
        return self.book_repository.get_all_books()

    def get_book_by_id(self, book_id):
        book = self.book_repository.get_book_by_id(book_id)
        if not book:
            raise ValueError("Libro no encontrado")
        return book

    def create_book(self, data):
        return self.book_repository.create_book(data)
    
    def update_book(self, book_id, data):
        book = self.book_repository.get_book_by_id(book_id)
        if not book:
            raise ValueError("Libro no encontrado")

        return self.book_repository.update_book(book, data)

    def delete_book(self, book_id):
        book = self.book_repository.get_book_by_id(book_id)
        if not book:
            raise ValueError("Libro no encontrado")
        self.book_repository.delete_book(book)
