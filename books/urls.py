from django.urls import path, include
from rest_framework.routers import DefaultRouter
from books.views.book_view import BookViewSet
from books.views.book_page_view import BookPageViewSet

router = DefaultRouter()
router.register("books", BookViewSet, basename="books")
router.register(r"books/(?P<book_id>\d+)/pages", BookPageViewSet, basename="bookpage")

urlpatterns = [
    path("", include(router.urls)),
]
