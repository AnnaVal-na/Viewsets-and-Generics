from rest_framework import serializers
from .models import Course, Lesson, Subscription
from .validators import validate_youtube_url


class LessonSerializer(serializers.ModelSerializer):
    """
    Сериализатор для урока.
    """

    # Применяем валидатор к полю video_url
    video_url = serializers.URLField(
        validators=[validate_youtube_url], required=False, allow_null=True
    )

    class Meta:
        model = Lesson
        fields = "__all__"


class SubscriptionSerializer(serializers.ModelSerializer):
    """
    Сериализатор для подписки.
    """

    class Meta:
        model = Subscription
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    """
    Сериализатор для курса:
    - Выводит количество уроков (lessons_count)
    - Выводит список уроков (lessons)
    - Показывает, подписан ли текущий пользователь (is_subscribed)
    """

    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = [
            "id",
            "title",
            "description",
            "owner",
            "lessons_count",
            "lessons",
            "is_subscribed",
        ]

    def get_lessons_count(self, obj):
        return obj.lessons.count()

    def get_is_subscribed(self, obj):
        user = self.context["request"].user
        if user.is_authenticated:
            return obj.subscriptions.filter(user=user).exists()
        return False
