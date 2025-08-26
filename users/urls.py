from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView  # Добавлен
from .views import PaymentViewSet, UserRegisterAPIView, UserListAPIView, UserRetrieveAPIView, UserUpdateAPIView, UserDestroyAPIView  # Добавлен новый View

router = DefaultRouter()
router.register(r'payments', PaymentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # ДОБАВЛЕНЫ эти пути:
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', UserRegisterAPIView.as_view(), name='register'),
    path('users/', UserListAPIView.as_view(), name='user-list'),
    path('users/<int:pk>/', UserRetrieveAPIView.as_view(), name='user-detail'),
    path('users/<int:pk>/update/', UserUpdateAPIView.as_view(), name='user-update'),
    path('users/<int:pk>/delete/', UserDestroyAPIView.as_view(), name='user-delete'),
]
