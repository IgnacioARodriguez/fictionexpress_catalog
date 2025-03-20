from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

class BookPage(models.Model):
    book = models.ForeignKey(Book, related_name="pages", on_delete=models.CASCADE)
    page_number = models.PositiveIntegerField()
    content = models.TextField()

    class Meta:
        ordering = ["page_number"]
        unique_together = ("book", "page_number")
