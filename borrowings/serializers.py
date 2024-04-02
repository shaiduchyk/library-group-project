from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from books_service.models import Book
from books_service.serializers import BookSerializer
from borrowings.models import Borrowing
from user.serializers import UserSerializer


class BorrowingSerializer(serializers.ModelSerializer):
    book = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all())
    actual_return_date = serializers.DateField(required=False, allow_null=True)

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
            "user"
        )

    def create(self, validated_data):
        with transaction.atomic():
            book_data = validated_data.pop("book")
            book = Book.objects.get(id=book_data.id)
            if book.inventory < 1:
                raise ValidationError("the following book is not available")
            borrowing = Borrowing.objects.create(**validated_data, book=book_data)
            book.inventory -= 1
            book.save()
            return borrowing


class BorrowingDetailSerializer(BorrowingSerializer):
    book = BookSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Book
        fields = (
            "id",
            "title",
            "author",
            "inventory",
            "book",
            "daily_fee",
        )


class BorrowingReturnSerializer(BorrowingSerializer):
    actual_return_date = serializers.DateField()
    borrow_date = serializers.DateField(read_only=True)
    book = BookSerializer(read_only=True)
    user = UserSerializer(read_only=True)
    expected_return_date = serializers.DateField(read_only=True)

    class Meta:
        model = Borrowing
        fields = (
            "actual_return_date",
            "borrow_date",
            "user",
            "expected_return_date",
            "book"
        )
