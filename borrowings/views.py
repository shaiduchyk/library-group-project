from django.db import transaction

from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError, PermissionDenied
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated

from borrowings.models import Borrowing
from borrowings.serializers import (
    BorrowingSerializer,
    BorrowingReturnSerializer,
    BorrowingDetailSerializer,
)


class BorrowingPagination(PageNumberPagination):
    page_size = 5
    max_page_size = 10


class BorrowingViewSet(
    GenericViewSet,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = BorrowingPagination

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


    @action(
        detail=True,
        methods=["post", "get"],
        url_path="return-borrowing"
    )

    def return_borrowing(self, request, pk=None):
        with transaction.atomic():
            borrowing = self.get_object()
            return_date = request.data.get("actual_return_date")
            if not return_date:
                serializer = self.get_serializer(borrowing)
                return Response(serializer.data)
            if borrowing.is_active:
                borrowing.actual_return_date = return_date
                book = borrowing.book
                book.inventory += 1
                book.save()
                borrowing.save()
                borrowing.create_fine_payment_if_overdue()
                serializer = self.get_serializer(borrowing)
                return Response(serializer.data)
            raise ValidationError("This borrowing is already finished")

    def get_queryset(self):
        user = self.request.user
        user_id = self.request.query_params.get("user_id")
        is_active = self.request.query_params.get("is_active")

        if user.is_superuser and user_id:
            queryset = Borrowing.objects.filter(user_id=user_id)
        elif user.is_superuser:
            queryset = Borrowing.objects.all()
        else:
            queryset = Borrowing.objects.filter(user_id=user.id)

        if is_active is not None:
            queryset = queryset.filter(
                actual_return_date__isnull=is_active == "True"
            )

        return queryset

    def get_serializer_class(self):
        if self.action == "retrieve":
            return BorrowingDetailSerializer

        if self.action == "return_borrowing":
            return BorrowingReturnSerializer

        return BorrowingSerializer
