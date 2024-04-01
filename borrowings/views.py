from rest_framework import generics, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated

from .models import Borrowing
from borrowings.serializers import (
    BorrowingSerializer,
)


class BorrowingViewSet(
    GenericViewSet,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer
    permission_classes = (IsAuthenticated,)

    @action(detail=True, methods=["post"])
    def return_borrowing(self, request, pk=None):
        borrowing = self.get_object()
        borrowing.actual_return_date = request.data.get("actual_return_date")
        borrowing.save()
        serializer = self.get_serializer(borrowing)
        return Response(serializer.data)

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
            queryset = queryset.filter(actual_return_date__isnull=is_active == "True")

        return queryset
