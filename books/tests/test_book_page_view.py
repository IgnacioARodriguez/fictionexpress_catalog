import pytest
from django.urls import reverse

@pytest.mark.django_db
def test_list_book_pages(api_client, create_book_with_pages):
    """Test to list pages of a book"""
    api_client.force_authenticate(user=create_book_with_pages.author)
    url = reverse("bookpage-list", kwargs={"book_id": create_book_with_pages.id})
    response = api_client.get(url)

    assert response.status_code == 200
    assert "results" in response.data
    assert len(response.data["results"]) > 0

@pytest.mark.django_db
def test_list_book_pages_unauthenticated(api_client, create_book_with_pages):
    """Test to list pages of a book without authentication"""
    url = reverse("bookpage-list", args=[create_book_with_pages.id])
    response = api_client.get(url)

    assert response.status_code == 401 

@pytest.mark.django_db
def test_list_pages_of_nonexistent_book(api_client, create_editor_user):
    """Test to list pages of a nonexistent book"""
    api_client.force_authenticate(user=create_editor_user)
    url = reverse("bookpage-list", args=[999])
    response = api_client.get(url)

    assert response.status_code == 404 

@pytest.mark.django_db
def test_list_book_pages_pagination(api_client, create_book_with_many_pages):
    """Test to list pages of a book with pagination"""
    api_client.force_authenticate(user=create_book_with_many_pages.author)
    url = reverse("bookpage-list", args=[create_book_with_many_pages.id])
    response = api_client.get(url, {"page": 1, "page_size": 5}) 

    assert response.status_code == 200
    assert "results" in response.data
    assert len(response.data["results"]) == 5

@pytest.mark.django_db
def test_list_book_pages_invalid_page(api_client, create_book_with_pages):
    """Test to list pages of a book with an invalid page number"""
    api_client.force_authenticate(user=create_book_with_pages.author)
    url = reverse("bookpage-list", args=[create_book_with_pages.id])
    response = api_client.get(url, {"page": 999})

    assert response.status_code == 404
