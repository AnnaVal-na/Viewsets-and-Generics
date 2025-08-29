from rest_framework import viewsets, permissions
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from courses.models import Course, Lesson
from courses.serializers import CourseSerializer, LessonSerializer
from users.permissions import IsModerator, IsOwner  # Добавить импорт


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['title', 'description']
    ordering_fields = ['created_at', 'title']


    def get_permissions(self):
        if self.action in ['create', 'destroy']:
            # Создавать и удалять могут только владельцы (не модераторы)
            self.permission_classes = [permissions.IsAuthenticated, ~IsModerator]
        elif self.action in ['update', 'partial_update']:
            # Редактировать могут модераторы, админы и владельцы
            self.permission_classes = [permissions.IsAuthenticated, IsModerator | permissions.IsAdminUser | IsOwner]
        else:
            # Просматривать могут все авторизованные
            self.permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in self.permission_classes]


    def perform_create(self, serializer):
        """Автоматически привязываем курс к текущему пользователю"""
        serializer.save(owner=self.request.user)


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['title', 'description', 'course']
    ordering_fields = ['created_at', 'title']


    def get_permissions(self):
        if self.action in ['create', 'destroy']:
            self.permission_classes = [permissions.IsAuthenticated, ~IsModerator]
        elif self.action in ['update', 'partial_update']:
            self.permission_classes = [permissions.IsAuthenticated, IsModerator | permissions.IsAdminUser | IsOwner]
        else:
            self.permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in self.permission_classes]


    def perform_create(self, serializer):
        """Автоматически привязываем урок к текущему пользователю"""
        serializer.save(owner=self.request.user)
