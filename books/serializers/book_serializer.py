from rest_framework import serializers
from books.models import Book
from books.serializers.book_page_serializer import BookPageSerializer

class BookSerializer(serializers.ModelSerializer):
    pages = BookPageSerializer(many=True, required=False)
    class Meta:
        model = Book
        fields = ["id", "title", "author", "created_at", "updated_at", "pages"]

    def validate_title(self, value):
        """Validate that the title is not empty"""
        if not value.strip():
            raise serializers.ValidationError("El título no puede estar vacío.")
        return value

    def validate_author(self, value):
        """Validate that the author is not empty"""
        if not value.strip():
            raise serializers.ValidationError("El autor no puede estar vacío.")
        return value
