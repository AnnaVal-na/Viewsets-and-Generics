from rest_framework import viewsets, permissions, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from django.shortcuts import get_object_or_404

from .models import Course, Lesson, Subscription
from .serializers import CourseSerializer, LessonSerializer
from .paginators import CourseLessonPagination
from users.permissions import IsOwner  # Убедитесь, что этот файл существует


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['title', 'description']
    ordering_fields = ['created_at', 'title']
    pagination_class = CourseLessonPagination

    def get_permissions(self):
        if self.action in ['create']:
            # Создавать могут только аутентифицированные пользователи (не staff)
            self.permission_classes = [permissions.IsAuthenticated, ~permissions.IsAdminUser]
        elif self.action in ['destroy']:
            # Удалять могут только владельцы и админы (не staff)
            self.permission_classes = [permissions.IsAuthenticated, ~permissions.IsAdminUser,
                                       IsOwner | permissions.IsAdminUser]
        elif self.action in ['update', 'partial_update']:
            # Редактировать могут staff, админы и владельцы
            self.permission_classes = [permissions.IsAuthenticated,
                                       permissions.IsAdminUser | permissions.IsAdminUser | IsOwner]
        else:
            # Просматривать могут все авторизованные
            self.permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in self.permission_classes]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['title', 'description', 'course']
    ordering_fields = ['created_at', 'title']
    pagination_class = CourseLessonPagination

    def get_permissions(self):
        if self.action in ['create']:
            self.permission_classes = [permissions.IsAuthenticated, ~permissions.IsAdminUser]
        elif self.action in ['destroy']:
            self.permission_classes = [permissions.IsAuthenticated, ~permissions.IsAdminUser,
                                       IsOwner | permissions.IsAdminUser]
        elif self.action in ['update', 'partial_update']:
            self.permission_classes = [permissions.IsAuthenticated,
                                       permissions.IsAdminUser | permissions.IsAdminUser | IsOwner]
        else:
            self.permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in self.permission_classes]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class SubscriptionAPIView(APIView):
    """
    APIView для управления подпиской на курс.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get('course_id')

        if not course_id:
            return Response(
                {"error": "course_id обязателен"},
                status=status.HTTP_400_BAD_REQUEST
            )

        course_item = get_object_or_404(Course, id=course_id)
        subscription = Subscription.objects.filter(
            user=user,
            course=course_item
        )

        if subscription.exists():
            subscription.delete()
            message = 'Подписка удалена'
        else:
            Subscription.objects.create(user=user, course=course_item)
            message = 'Подписка добавлена'

        return Response({"message": message}, status=status.HTTP_200_OK)
