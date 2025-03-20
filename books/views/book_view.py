from rest_framework import viewsets, status
from rest_framework.response import Response
from books.services.book_service import BookService
from books.serializers.book_serializer import BookSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from books.permissions.book_permissions import IsEditorOrReadOnly

class BookViewSet(viewsets.ViewSet):
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated, IsEditorOrReadOnly]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.book_service = BookService()

    def list(self, request):
            try:
                books = self.book_service.get_books()

                if not books.exists():
                    return Response({"message": "No hay libros disponibles"}, status=status.HTTP_204_NO_CONTENT)

                paginator = PageNumberPagination()
                paginated_books = paginator.paginate_queryset(books, request)

                return paginator.get_paginated_response(BookSerializer(paginated_books, many=True).data)

            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, pk=None):
        try:
            book = self.book_service.get_book_by_id(pk)
            return Response(BookSerializer(book).data)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request):
        try:
            book = self.book_service.create_book(request.data)
            return Response(BookSerializer(book).data, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, pk=None):
        try:
            self.book_service.delete_book(pk)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
