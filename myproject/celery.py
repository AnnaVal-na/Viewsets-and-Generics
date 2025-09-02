import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

app = Celery('myproject')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'check-updates-every-30-minutes': {
        'task': 'courses.tasks.check_course_updates',
        'schedule': 1800.0,  # 30 минут
    },
}
