from rest_framework import serializers
from urllib.parse import urlparse


def validate_youtube_url(value):
    """
    Валидатор, проверяющий, что ссылка ведет только на youtube.com.
    """
    if value:  # Проверяем только если значение не пустое
        parsed_url = urlparse(value)
        # Проверяем, что домен именно 'youtube.com', 'www.youtube.com' или 'youtu.be'
        if parsed_url.hostname not in ["youtube.com", "www.youtube.com", "youtu.be"]:
            raise serializers.ValidationError("Разрешены только ссылки на youtube.com")
    return value
