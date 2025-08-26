from rest_framework import serializers
from .models import Course, Lesson

class LessonSerializer(serializers.ModelSerializer):
    """
    Сериализатор для урока.
    """
    class Meta:
        model = Lesson
        fields = '__all__'  # Исправлено: включаем ВСЕ поля, включая course и owner


class CourseSerializer(serializers.ModelSerializer):
    """
    Сериализатор для курса:
    - Выводит количество уроков (lessons_count)
    - Выводит список уроков (lessons)
    """
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = [
            'id',
            'title',
            'description',
            'owner',
            'lessons_count',
            'lessons',
        ]

    def get_lessons_count(self, obj):
        return obj.lessons.count()
