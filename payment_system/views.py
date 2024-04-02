from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAdminUser

from payment_system.models import Payment
from .serializers import PaymentSerializer


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
