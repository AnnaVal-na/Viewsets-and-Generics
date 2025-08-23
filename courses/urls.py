from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, LessonViewSet  # Импортируем оба ViewSet

# Создаём роутер
router = DefaultRouter()
router.register(r'courses', CourseViewSet)
router.register(r'lessons', LessonViewSet)

# Все маршруты берутся из роутера
urlpatterns = [
    path('', include(router.urls)),
]
