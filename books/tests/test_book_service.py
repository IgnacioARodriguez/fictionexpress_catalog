import pytest
from unittest.mock import patch
from rest_framework.exceptions import NotFound, ValidationError

@pytest.mark.django_db
def test_get_books(book_service):
    """Test that get_books returns all books"""
    service, mock_repo = book_service
    mock_repo.get_all_books.return_value = ["Book 1", "Book 2"]

    books = service.get_books()
    assert books == ["Book 1", "Book 2"]
    mock_repo.get_all_books.assert_called_once()

@pytest.mark.django_db
def test_get_book_by_id_found(book_service):
    """Test that get_book_by_id returns a book if it exists"""
    service, mock_repo = book_service
    mock_repo.get_book_by_id.return_value = "Book Found"

    book = service.get_book_by_id(1)
    assert book == "Book Found"
    mock_repo.get_book_by_id.assert_called_once_with(1)

@pytest.mark.django_db
def test_get_book_by_id_not_found(book_service):
    """Test that get_book_by_id raises NotFound if the book does not exist"""
    service, mock_repo = book_service
    mock_repo.get_book_by_id.return_value = None

    with pytest.raises(NotFound, match="Book not found"):
        service.get_book_by_id(999)

@pytest.mark.django_db
def test_create_book_valid(book_service):
    """Test the creation of a book with valid data"""
    service, mock_repo = book_service
    mock_repo.create_book.return_value = {"title": "New Book", "author": "New Author"}

    book = service.create_book({"title": "New Book", "author": "New Author"})
    assert book["title"] == "New Book"
    mock_repo.create_book.assert_called_once()

@pytest.mark.django_db
def test_create_book_invalid(book_service):
    """Test that create_book raises ValidationError if the data is invalid"""
    service, mock_repo = book_service

    with pytest.raises(ValidationError):
        service.create_book({"title": ""})

@pytest.mark.django_db
def test_update_book_valid(book_service):
    """Test the update of a book with valid data"""
    service, mock_repo = book_service
    mock_repo.get_book_by_id.return_value = {"title": "Existing Book"}
    mock_repo.update_book.return_value = {"title": "Modified Book"}

    book = service.update_book(1, {"title": "Modified Book"})
    assert book["title"] == "Modified Book"
    mock_repo.get_book_by_id.assert_called_once_with(1)
    mock_repo.update_book.assert_called_once()

@pytest.mark.django_db
def test_update_book_not_found(book_service):
    """Test that update_book raises NotFound if the book does not exist"""
    service, mock_repo = book_service
    mock_repo.get_book_by_id.return_value = None

    with pytest.raises(NotFound, match="Book not found"):
        service.update_book(999, {"title": "Attempted Change"})

@pytest.mark.django_db
def test_delete_book_valid(book_service):
    """Test that delete_book deletes an existing book"""
    service, mock_repo = book_service
    mock_repo.get_book_by_id.return_value = {"title": "Book to Delete"}

    service.delete_book(1)
    mock_repo.get_book_by_id.assert_called_once_with(1)
    mock_repo.delete_book.assert_called_once()

@pytest.mark.django_db
def test_delete_book_not_found(book_service):
    """Test that delete_book raises NotFound if the book does not exist"""
    service, mock_repo = book_service
    mock_repo.get_book_by_id.return_value = None

    with pytest.raises(NotFound, match="Book not found"):
        service.delete_book(999)
