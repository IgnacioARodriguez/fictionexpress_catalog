import pytest
from django.urls import reverse

@pytest.mark.django_db
def test_list_books(api_client, create_books, create_reader_user):
    """Prueba obtener la lista de libros paginada"""
    api_client.force_authenticate(user=create_reader_user)
    url = reverse("books-list")
    response = api_client.get(url)
    assert response.status_code == 200
    assert "results" in response.data
    assert len(response.data["results"]) > 0

@pytest.mark.django_db
def test_list_books_unauthenticated(api_client):
    """Prueba que un usuario no autenticado no pueda listar libros"""
    url = reverse("books-list")
    response = api_client.get(url)
    assert response.status_code == 401

@pytest.mark.django_db
def test_create_book_as_editor(api_client, create_editor_user):
    """Prueba la creación de un libro como editor"""
    api_client.force_authenticate(user=create_editor_user)
    url = reverse("books-list")
    data = {"title": "Nuevo Libro", "author": "Nuevo Autor"}
    response = api_client.post(url, data)
    assert response.status_code == 201
    assert response.data["title"] == "Nuevo Libro"

@pytest.mark.django_db
def test_create_book_as_reader(api_client, create_reader_user):
    """Prueba que un reader no pueda crear libros"""
    api_client.force_authenticate(user=create_reader_user)
    url = reverse("books-list")
    data = {"title": "Nuevo Libro", "author": "Nuevo Autor"}
    response = api_client.post(url, data)
    assert response.status_code == 403 

@pytest.mark.django_db
def test_update_book_as_editor(api_client, create_editor_user, create_books):
    """Prueba que un editor pueda actualizar un libro"""
    api_client.force_authenticate(user=create_editor_user)
    url = reverse("books-detail", args=[create_books[0].id])
    data = {"title": "Título Modificado", "author": "Autor Modificado"}
    response = api_client.put(url, data)
    assert response.status_code == 200
    assert response.data["title"] == "Título Modificado"

@pytest.mark.django_db
def test_update_book_as_reader(api_client, create_reader_user, create_books):
    """Prueba que un reader NO pueda actualizar libros"""
    api_client.force_authenticate(user=create_reader_user)
    url = reverse("books-detail", args=[create_books[0].id])
    data = {"title": "Intento de Cambio"}
    response = api_client.put(url, data)
    assert response.status_code == 403 

@pytest.mark.django_db
def test_update_book_invalid_data(api_client, create_editor_user, create_books):
    """Prueba que un editor NO pueda actualizar un libro con datos inválidos"""
    api_client.force_authenticate(user=create_editor_user)
    url = reverse("books-detail", args=[create_books[0].id])
    data = {"title": ""}
    response = api_client.put(url, data)
    print('ACA', response.data)
    assert response.status_code == 400

@pytest.mark.django_db
def test_delete_book_as_editor(api_client, create_editor_user, create_books):
    """Prueba que un editor pueda eliminar un libro"""
    api_client.force_authenticate(user=create_editor_user)
    url = reverse("books-detail", args=[create_books[0].id])
    response = api_client.delete(url)
    assert response.status_code == 204

@pytest.mark.django_db
def test_delete_book_as_reader(api_client, create_reader_user, create_books):
    """Prueba que un reader NO pueda eliminar libros"""
    api_client.force_authenticate(user=create_reader_user)
    url = reverse("books-detail", args=[create_books[0].id])
    response = api_client.delete(url)
    assert response.status_code == 403 

@pytest.mark.django_db
def test_delete_book_unauthenticated(api_client, create_books):
    """Prueba que un usuario no autenticado NO pueda eliminar libros"""
    url = reverse("books-detail", args=[create_books[0].id])
    response = api_client.delete(url)
    assert response.status_code == 401 


