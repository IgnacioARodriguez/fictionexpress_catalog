from django.urls import path, include
from rest_framework.routers import DefaultRouter
from books.views.book_view import BookViewSet
from books.views.book_page_view import BookPageViewSet

router = DefaultRouter()
router.register("books", BookViewSet, basename="books")

urlpatterns = [
    path("", include(router.urls)),
    path("books/<int:book_id>/pages/", BookPageViewSet.as_view({"get": "list"})),
]
