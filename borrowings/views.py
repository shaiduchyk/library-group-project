from rest_framework import generics, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .models import Borrowing
from borrowings.serializers import BorrowingSerializer


class BorrowingViewSet(
    GenericViewSet,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer

    @action(detail=True, methods=["post"])
    def return_borrowing(self, request, pk=None):
        borrowing = self.get_object()
        borrowing.actual_return_date = request.data.get("actual_return_date")
        borrowing.save()
        serializer = self.get_serializer(borrowing)
        return Response(serializer.data)
