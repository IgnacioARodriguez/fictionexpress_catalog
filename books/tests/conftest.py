import pytest
from django.contrib.auth import get_user_model
from books.models import Book, BookPage
from django.conf import settings
import django

User = get_user_model()

@pytest.fixture
def api_client():
    """Cliente de pruebas para la API"""
    from rest_framework.test import APIClient
    return APIClient()

@pytest.fixture
def create_editor_user(db):
    """Crea un usuario con rol editor"""
    return User.objects.create_user(username="editor", email="editor@example.com", password="password123", role="editor")

@pytest.fixture
def create_reader_user(db):
    """Crea un usuario con rol reader"""
    return User.objects.create_user(username="reader", email="reader@example.com", password="password123", role="reader")

@pytest.fixture
def create_books(db):
    """Crea libros de prueba"""
    book1 = Book.objects.create(title="Libro 1", author="Autor 1")
    book2 = Book.objects.create(title="Libro 2", author="Autor 2")
    return [book1, book2]

@pytest.fixture
def create_book_with_pages(db, create_editor_user):
    """Crea un libro con 2 páginas de prueba y lo asigna a un usuario real"""
    book = Book.objects.create(title="Libro con Páginas", author=create_editor_user)
    BookPage.objects.create(book=book, page_number=1, content="Contenido de la página 1")
    BookPage.objects.create(book=book, page_number=2, content="Contenido de la página 2")
    return book


@pytest.fixture
def create_book_with_many_pages(db, create_editor_user):
    """Crea un libro con muchas páginas para probar la paginación"""
    book = Book.objects.create(title="Libro con Muchas Páginas", author=create_editor_user)
    for i in range(1, 21): 
        BookPage.objects.create(book=book, page_number=i, content=f"Contenido de la página {i}")
    return book
