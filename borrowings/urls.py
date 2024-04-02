from django.urls import path, include
from rest_framework import routers

from borrowings.views import (
    BorrowingViewSet
)

from rest_framework.routers import DefaultRouter

# router = DefaultRouter()
# router.register(r"", BorrowingViewSet, basename='borrowings')
#
# urlpatterns = [
#     path("", include(router.urls)),
# ]
#
# app_name = "borrowings"


router = routers.DefaultRouter()
router.register("", BorrowingViewSet)

urlpatterns = [path("", include(router.urls))]

app_name = "borrowings"
