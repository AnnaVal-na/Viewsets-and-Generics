from rest_framework import viewsets
from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer


class CourseViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления курсами:
    GET /api/courses/ — список
    POST /api/courses/ — создание
    GET /api/courses/1/ — детали
    PUT/PATCH /api/courses/1/ — редактирование
    DELETE /api/courses/1/ — удаление
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class LessonViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления уроками (аналогично курсам)
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
