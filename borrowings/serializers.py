from rest_framework import serializers
from books_service.models import Book
from books_service.serializers import BookSerializer
from borrowings.models import Borrowing
from user.serializers import UserSerializer


class BorrowingSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=False, allow_null=False)

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
        books_data = validated_data.pop("books")
        borrowing = Borrowing.objects.create(**validated_data)
        for book_data in books_data:
            book = Book.objects.create(borrowing=borrowing, **book_data)
            borrowing.book.add(book)
        return borrowing


class BorrowingDetailSerializer(BorrowingSerializer):
    book = BookSerializer(many=True, read_only=True)
    user = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Book
        fields = (
            "id",
            "title",
            "author",
            "inventory",
            "daily_fee",
        )
