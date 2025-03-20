import pytest
from django.urls import reverse

@pytest.mark.django_db
def test_list_books(api_client, create_books, create_reader_user):
    """Test to get the paginated list of books"""
    api_client.force_authenticate(user=create_reader_user)
    url = reverse("books-list")
    response = api_client.get(url)
    assert response.status_code == 200
    assert "results" in response.data
    assert len(response.data["results"]) > 0

@pytest.mark.django_db
def test_list_books_unauthenticated(api_client):
    """Test that an unauthenticated user cannot list books"""
    url = reverse("books-list")
    response = api_client.get(url)
    assert response.status_code == 401

@pytest.mark.django_db
def test_create_book_as_editor(api_client, create_editor_user):
    """Test book creation as an editor"""
    api_client.force_authenticate(user=create_editor_user)
    url = reverse("books-list")
    data = {"title": "New Book", "author": "New Author"}
    response = api_client.post(url, data)
    assert response.status_code == 201
    assert response.data["title"] == "New Book"

@pytest.mark.django_db
def test_create_book_as_reader(api_client, create_reader_user):
    """Test that a reader cannot create books"""
    api_client.force_authenticate(user=create_reader_user)
    url = reverse("books-list")
    data = {"title": "New Book", "author": "New Author"}
    response = api_client.post(url, data)
    assert response.status_code == 403 

@pytest.mark.django_db
def test_update_book_as_editor(api_client, create_editor_user, create_books):
    """Test that an editor can update a book"""
    api_client.force_authenticate(user=create_editor_user)
    url = reverse("books-detail", args=[create_books[0].id])
    data = {"title": "Modified Title", "author": "Modified Author"}
    response = api_client.put(url, data)
    assert response.status_code == 200
    assert response.data["title"] == "Modified Title"

@pytest.mark.django_db
def test_update_book_as_reader(api_client, create_reader_user, create_books):
    """Test that a reader cannot update books"""
    api_client.force_authenticate(user=create_reader_user)
    url = reverse("books-detail", args=[create_books[0].id])
    data = {"title": "Attempted Change"}
    response = api_client.put(url, data)
    assert response.status_code == 403 

@pytest.mark.django_db
def test_update_book_invalid_data(api_client, create_editor_user, create_books):
    """Test that an editor cannot update a book with invalid data"""
    api_client.force_authenticate(user=create_editor_user)
    url = reverse("books-detail", args=[create_books[0].id])
    data = {"title": ""}
    response = api_client.put(url, data)
    print('HERE', response.data)
    assert response.status_code == 400

@pytest.mark.django_db
def test_delete_book_as_editor(api_client, create_editor_user, create_books):
    """Test that an editor can delete a book"""
    api_client.force_authenticate(user=create_editor_user)
    url = reverse("books-detail", args=[create_books[0].id])
    response = api_client.delete(url)
    assert response.status_code == 204

@pytest.mark.django_db
def test_delete_book_as_reader(api_client, create_reader_user, create_books):
    """Test that a reader cannot delete books"""
    api_client.force_authenticate(user=create_reader_user)
    url = reverse("books-detail", args=[create_books[0].id])
    response = api_client.delete(url)
    assert response.status_code == 403 

@pytest.mark.django_db
def test_delete_book_unauthenticated(api_client, create_books):
    """Test that an unauthenticated user cannot delete books"""
    url = reverse("books-detail", args=[create_books[0].id])
    response = api_client.delete(url)
    assert response.status_code == 401 
