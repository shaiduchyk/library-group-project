from rest_framework import generics
from .models import Borrowing
from .serializers import DetailedBookSerializer


class BorrowingListView(generics.ListAPIView):
    queryset = Borrowing.objects.all()
    serializer_class = DetailedBookSerializer


class BorrowingDetailView(generics.RetrieveAPIView):
    queryset = Borrowing.objects.all()
    serializer_class = DetailedBookSerializer
