import pytest
from unittest.mock import patch
from rest_framework.exceptions import NotFound, ValidationError

@pytest.mark.django_db
def test_get_books(book_service):
    """Prueba que get_books retorne todos los libros"""
    service, mock_repo = book_service
    mock_repo.get_all_books.return_value = ["Libro 1", "Libro 2"]

    books = service.get_books()
    assert books == ["Libro 1", "Libro 2"]
    mock_repo.get_all_books.assert_called_once()

@pytest.mark.django_db
def test_get_book_by_id_found(book_service):
    """Prueba que get_book_by_id retorne un libro si existe"""
    service, mock_repo = book_service
    mock_repo.get_book_by_id.return_value = "Libro Encontrado"

    book = service.get_book_by_id(1)
    assert book == "Libro Encontrado"
    mock_repo.get_book_by_id.assert_called_once_with(1)

@pytest.mark.django_db
def test_get_book_by_id_not_found(book_service):
    """Prueba que get_book_by_id lance NotFound si el libro no existe"""
    service, mock_repo = book_service
    mock_repo.get_book_by_id.return_value = None

    with pytest.raises(NotFound, match="Libro no encontrado"):
        service.get_book_by_id(999)

@pytest.mark.django_db
def test_create_book_valid(book_service):
    """Prueba la creación de un libro con datos válidos"""
    service, mock_repo = book_service
    mock_repo.create_book.return_value = {"title": "Nuevo Libro", "author": "Nuevo Autor"}

    book = service.create_book({"title": "Nuevo Libro", "author": "Nuevo Autor"})
    assert book["title"] == "Nuevo Libro"
    mock_repo.create_book.assert_called_once()

@pytest.mark.django_db
def test_create_book_invalid(book_service):
    """Prueba que create_book lance ValidationError si los datos son inválidos"""
    service, mock_repo = book_service

    with pytest.raises(ValidationError):
        service.create_book({"title": ""})

@pytest.mark.django_db
def test_update_book_valid(book_service):
    """Prueba la actualización de un libro con datos válidos"""
    service, mock_repo = book_service
    mock_repo.get_book_by_id.return_value = {"title": "Libro Existente"}
    mock_repo.update_book.return_value = {"title": "Libro Modificado"}

    book = service.update_book(1, {"title": "Libro Modificado"})
    assert book["title"] == "Libro Modificado"
    mock_repo.get_book_by_id.assert_called_once_with(1)
    mock_repo.update_book.assert_called_once()

@pytest.mark.django_db
def test_update_book_not_found(book_service):
    """Prueba que update_book lance NotFound si el libro no existe"""
    service, mock_repo = book_service
    mock_repo.get_book_by_id.return_value = None

    with pytest.raises(NotFound, match="Libro no encontrado"):
        service.update_book(999, {"title": "Intento de Cambio"})

@pytest.mark.django_db
def test_delete_book_valid(book_service):
    """Prueba que delete_book elimine un libro existente"""
    service, mock_repo = book_service
    mock_repo.get_book_by_id.return_value = {"title": "Libro a Eliminar"}

    service.delete_book(1)
    mock_repo.get_book_by_id.assert_called_once_with(1)
    mock_repo.delete_book.assert_called_once()

@pytest.mark.django_db
def test_delete_book_not_found(book_service):
    """Prueba que delete_book lance NotFound si el libro no existe"""
    service, mock_repo = book_service
    mock_repo.get_book_by_id.return_value = None

    with pytest.raises(NotFound, match="Libro no encontrado"):
        service.delete_book(999)

