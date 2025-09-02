from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import Course, Subscription


@shared_task
def send_course_update_email(course_id, update_message):
    """
    Отправка email подписчикам курса об обновлении
    """
    try:
        course = Course.objects.get(id=course_id)
        subscriptions = Subscription.objects.filter(course=course)

        for subscription in subscriptions:
            subject = f'Обновление курса: {course.title}'
            message = f'''
            Здравствуйте, {subscription.user.email}!

            Курс "{course.title}" был обновлен:
            {update_message}

            Перейти к курсу: http://localhost:8000/api/courses/{course.id}/
            '''

            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[subscription.user.email],
                fail_silently=False,
            )

        return f"Отправлено писем: {subscriptions.count()}"

    except Course.DoesNotExist:
        return "Курс не найден"


@shared_task
def check_course_updates():
    """
    Периодическая задача для проверки обновлений курсов
    """

    return "Проверка обновлений выполнена"
