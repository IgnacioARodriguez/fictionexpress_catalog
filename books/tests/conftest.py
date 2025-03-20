import pytest
from django.contrib.auth import get_user_model
from books.models import Book, BookPage
from unittest.mock import patch
from books.services.book_service import BookService
from rest_framework.test import APIClient

User = get_user_model()

@pytest.fixture
def api_client():
    """Create an instance of the Django test client"""
    return APIClient()

@pytest.fixture
def create_editor_user(db):
    """Create a user with editor role"""
    return User.objects.create_user(username="editor", email="editor@example.com", password="password123", role="editor")

@pytest.fixture
def create_reader_user(db):
    """Create a user with reader role"""
    return User.objects.create_user(username="reader", email="reader@example.com", password="password123", role="reader")

@pytest.fixture
def create_books(db):
    """Create two books to test the list view"""
    book1 = Book.objects.create(title="Libro 1", author="Autor 1")
    book2 = Book.objects.create(title="Libro 2", author="Autor 2")
    return [book1, book2]

@pytest.fixture
def create_book_with_pages(db, create_editor_user):
    """Crear un libro con páginas para probar la relación uno a muchos"""
    book = Book.objects.create(title="Libro con Páginas", author=create_editor_user)
    BookPage.objects.create(book=book, page_number=1, content="Contenido de la página 1")
    BookPage.objects.create(book=book, page_number=2, content="Contenido de la página 2")
    return book


@pytest.fixture
def create_book_with_many_pages(db, create_editor_user):
    """Create a book with many pages to test the one-to-many relationship"""
    book = Book.objects.create(title="Libro con Muchas Páginas", author=create_editor_user)
    for i in range(1, 21): 
        BookPage.objects.create(book=book, page_number=i, content=f"Contenido de la página {i}")
    return book

@pytest.fixture
def book_service():
    """Creates a BookService instance with a mocked repository."""
    with patch("books.services.book_service.BookRepository") as MockRepo:
        mock_repo = MockRepo.return_value
        service = BookService()
        service.book_repository = mock_repo
        return service, mock_repo
    
@pytest.fixture
def editor_user(db):
    """Create a user with editor role"""
    return User.objects.create_user(username="editor", email="editor@example.com", password="password123", role="editor")

@pytest.fixture
def reader_user(db):
    """Create a user with reader role"""
    return User.objects.create_user(username="reader", email="reader@example.com", password="password123", role="reader")
