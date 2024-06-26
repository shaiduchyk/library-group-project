from rest_framework import mixins, viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from payment_system.models import Payment
from payment_system.serializers import PaymentSerializer


class PaymentViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = PaymentSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            if IsAdminUser().has_permission(self.request, self):
                return Payment.objects.all()
            return Payment.objects.filter(borrowing__user=user)
        return Payment.objects.none()

    @action(
        detail=False,
        methods=["get"],
        url_path="success"
    )
    def success(self, request, pk=None):
        return Response(
                {"message": "Payment marked as paid."},
                status=status.HTTP_200_OK
            )

    @action(detail=False, methods=["get"])
    def cancel(self, request, pk=None):
        return Response(
            {"message": "You have cancer"},
            status=status.HTTP_200_OK
        )
