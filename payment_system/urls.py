from django.urls import path, include
from rest_framework import routers

from payment_system.views import PaymentViewSet

router = routers.DefaultRouter()
router.register("", PaymentViewSet, basename="payments")

urlpatterns = [path("", include(router.urls))]

app_name = "payments"
