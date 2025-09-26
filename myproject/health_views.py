from django.http import JsonResponse
from django.views import View
from django.db import connection
from django.utils import timezone
from django.conf import settings
from redis import Redis
from redis.exceptions import ConnectionError as RedisConnectionError
import logging

logger = logging.getLogger(__name__)


class HealthCheckView(View):
    """
    Health check endpoint for Docker and load balancers
    """

    def get(self, request):
        # Проверка базы данных
        db_status = self.check_database()

        # Проверка Redis
        redis_status = self.check_redis()

        # Общий статус
        overall_status = db_status and redis_status

        status_code = 200 if overall_status else 503

        return JsonResponse(
            {
                "status": "healthy" if overall_status else "unhealthy",
                "database": "connected" if db_status else "disconnected",
                "redis": "connected" if redis_status else "disconnected",
                "timestamp": str(timezone.now()),
            },
            status=status_code,
        )

    def check_database(self):
        """Проверка подключения к базе данных"""
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
            return True
        except Exception as e:
            logger.error(f"Database health check failed: {e}")
            return False

    def check_redis(self):
        """Проверка подключения к Redis"""
        try:
            redis_client = Redis.from_url(
                settings.CELERY_BROKER_URL, socket_connect_timeout=1, socket_timeout=1
            )
            redis_client.ping()
            return True
        except RedisConnectionError as e:
            logger.error(f"Redis health check failed: {e}")
            return False
        except Exception as e:
            logger.error(f"Redis health check error: {e}")
            return False
