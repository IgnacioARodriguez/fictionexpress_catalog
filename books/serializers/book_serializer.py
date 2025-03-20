from rest_framework import serializers
from books.models import Book
from books.serializers.book_page_serializer import BookPageSerializer

class BookSerializer(serializers.ModelSerializer):
    pages = BookPageSerializer(many=True, read_only=True)

    class Meta:
        model = Book
        fields = ["id", "title", "author", "created_at", "updated_at", "pages"]
