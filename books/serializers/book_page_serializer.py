from rest_framework import serializers
from books.models import BookPage

class BookPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookPage
        fields = ["page_number", "content"]

    def validate_page_number(self, value):
        """Validate that the page number is not negative"""
        if value < 0:
            raise serializers.ValidationError("El número de página no puede ser negativo.")
        return value
    
    def validate_content(self, value):
        """Validate that the content is not empty"""
        if not value.strip():
            raise serializers.ValidationError("El contenido no puede estar vacío.")
        return value