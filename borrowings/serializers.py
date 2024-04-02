from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from books_service.models import Book

from borrowings.models import Borrowing
from payment_system.serializers import PaymentSerializer


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('id', 'title', 'author', 'inventory')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'email')


class BorrowingSerializer(serializers.ModelSerializer):
    book = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all())
    actual_return_date = serializers.DateField(read_only=True, required=False, allow_null=True)
    payments = PaymentSerializer(many=True, read_only=True, source="payment_set")

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
            "user",
            "payments",
        )

    def validate(self, attrs):
        borrow_date = attrs.get("borrow_date")
        expected_return_date = attrs.get("expected_return_date")
        if borrow_date and expected_return_date and expected_return_date < borrow_date:
            raise serializers.ValidationError("Expected return date cannot be earlier than borrow date.")
        return attrs

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
    book = BookSerializer()
    user = UserSerializer()

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
