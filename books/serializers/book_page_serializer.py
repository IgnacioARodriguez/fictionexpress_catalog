from rest_framework import serializers
from books.models import BookPage

class BookPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookPage
        fields = ["page_number", "content"]