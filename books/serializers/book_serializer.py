from rest_framework import serializers
from books.models import Book
from books.serializers.book_page_serializer import BookPageSerializer

class BookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = ["id", "title", "author", "created_at", "updated_at"]
