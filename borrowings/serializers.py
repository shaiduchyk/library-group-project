from rest_framework import serializers
from books_service.models import Book


class DetailedBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = (
            "id",
            "title",
            "author",
            "inventory",
            "daily_fee",
        )
