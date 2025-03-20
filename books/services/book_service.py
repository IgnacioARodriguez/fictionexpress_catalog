from books.repositories.book_repository import BookRepository
from books.serializers.book_serializer import BookSerializer
from rest_framework.exceptions import NotFound


class BookService:
    def __init__(self):
        self.book_repository = BookRepository()

    def get_books(self):
        return self.book_repository.get_all_books()

    def get_book_by_id(self, book_id):
        book = self.book_repository.get_book_by_id(book_id)
        if not book:
            raise NotFound("Libro no encontrado")
        return book

    def create_book(self, data):
        """
        Valida y crea un nuevo libro.
        """
        serializer = BookSerializer(data=data)
        serializer.is_valid(raise_exception=True)  # 🔹 Validamos aquí
        return self.book_repository.create_book(serializer.validated_data)
    
    def update_book(self, book_id, data):
        """
        Valida y actualiza un libro existente.
        """
        book = self.get_book_by_id(book_id)  # 🔹 Verificamos que el libro existe
        serializer = BookSerializer(book, data=data, partial=True)
        serializer.is_valid(raise_exception=True)  # 🔹 Validamos los datos actualizados
        return self.book_repository.update_book(book, serializer.validated_data)

    def delete_book(self, book_id):
        book = self.book_repository.get_book_by_id(book_id)
        if not book:
            raise NotFound("Libro no encontrado")
        self.book_repository.delete_book(book)
