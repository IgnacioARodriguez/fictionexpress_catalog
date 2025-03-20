import pytest
from django.urls import reverse

@pytest.mark.django_db
def test_list_book_pages(api_client, create_book_with_pages):
    """Prueba obtener las páginas de un libro con paginación"""
    api_client.force_authenticate(user=create_book_with_pages.author)
    url = reverse("bookpage-list", kwargs={"book_id": create_book_with_pages.id})
    response = api_client.get(url)

    assert response.status_code == 200
    assert "results" in response.data
    assert len(response.data["results"]) > 0

@pytest.mark.django_db
def test_list_book_pages_unauthenticated(api_client, create_book_with_pages):
    """Prueba que un usuario no autenticado no pueda ver páginas de un libro"""
    url = reverse("bookpage-list", args=[create_book_with_pages.id])
    response = api_client.get(url)

    assert response.status_code == 401 

@pytest.mark.django_db
def test_list_pages_of_nonexistent_book(api_client, create_editor_user):
    """Prueba que obtener páginas de un libro inexistente retorne 404"""
    api_client.force_authenticate(user=create_editor_user)
    url = reverse("bookpage-list", args=[999])  # ID inexistente
    response = api_client.get(url)

    assert response.status_code == 404 

@pytest.mark.django_db
def test_list_book_pages_pagination(api_client, create_book_with_many_pages):
    """Prueba que las páginas de un libro sean paginadas correctamente"""
    api_client.force_authenticate(user=create_book_with_many_pages.author)
    url = reverse("bookpage-list", args=[create_book_with_many_pages.id])
    response = api_client.get(url, {"page": 1, "page_size": 5}) 

    assert response.status_code == 200
    assert "results" in response.data
    assert len(response.data["results"]) == 5

@pytest.mark.django_db
def test_list_book_pages_invalid_page(api_client, create_book_with_pages):
    """Prueba que solicitar una página inexistente devuelva error"""
    api_client.force_authenticate(user=create_book_with_pages.author)
    url = reverse("bookpage-list", args=[create_book_with_pages.id])
    response = api_client.get(url, {"page": 999})

    assert response.status_code == 404
