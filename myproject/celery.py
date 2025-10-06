import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")

app = Celery("myproject")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.beat_schedule = {
    # Проверка обновлений курсов каждые 30 минут
    "check-updates-every-30-minutes": {
        "task": "courses.tasks.check_course_updates",
        "schedule": 1800.0,  # 30 минут
    },
    # Проверка неактивных пользователей каждый день в 8:00 утра
    "check-inactive-users-daily": {
        "task": "users.tasks.check_inactive_users",
        "schedule": crontab(hour=8, minute=0),  # Ежедневно в 8:00
    },
}

app.conf.timezone = "Europe/Moscow"
