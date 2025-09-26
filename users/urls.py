from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PaymentViewSet,
    UserRegisterAPIView,
    UserListAPIView,
    UserRetrieveAPIView,
    UserUpdateAPIView,
    UserDestroyAPIView,
    CreatePaymentAPIView,
    PaymentStatusAPIView,
)

router = DefaultRouter()
router.register(r"payments", PaymentViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("register/", UserRegisterAPIView.as_view(), name="user-register"),
    path("users/", UserListAPIView.as_view(), name="user-list"),
    path("users/<int:pk>/", UserRetrieveAPIView.as_view(), name="user-detail"),
    path("users/<int:pk>/update/", UserUpdateAPIView.as_view(), name="user-update"),
    path("users/<int:pk>/delete/", UserDestroyAPIView.as_view(), name="user-delete"),
    # Новые пути для оплаты
    path("payment/create/", CreatePaymentAPIView.as_view(), name="payment-create"),
    path(
        "payment/<int:payment_id>/status/",
        PaymentStatusAPIView.as_view(),
        name="payment-status",
    ),
]
