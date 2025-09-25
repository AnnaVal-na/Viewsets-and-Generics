from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()


@shared_task
def check_inactive_users():
    """
    Проверяет пользователей, которые не заходили более месяца и блокирует их
    """
    try:
        # Находим пользователей, которые не заходили более 30 дней
        month_ago = timezone.now() - timezone.timedelta(days=30)
        inactive_users = User.objects.filter(last_login__lt=month_ago, is_active=True)

        # Блокируем неактивных пользователей
        count = inactive_users.update(is_active=False)

        # Отправляем уведомление администратору
        if count > 0:
            try:
                send_mail(
                    subject="Отчет о блокировке неактивных пользователей",
                    message=f"Было заблокировано {count} неактивных пользователей, которые не заходили более месяца.",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.ADMIN_EMAIL],
                    fail_silently=True,
                )
            except Exception as email_error:
                # Если отправка email не удалась, продолжаем работу
                pass

        return f"Заблокировано {count} неактивных пользователей"

    except Exception as e:
        # Логируем ошибку, но не прерываем выполнение
        return f"Ошибка при блокировке пользователей: {str(e)}"


@shared_task
def send_user_notification(user_id, message):
    """
    Отправка уведомления пользователю (может пригодиться для будущих задач)
    """
    try:
        user = User.objects.get(id=user_id)
        send_mail(
            subject="Уведомление от образовательной платформы",
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=True,
        )
        return f"Уведомление отправлено пользователю {user.email}"
    except User.DoesNotExist:
        return "Пользователь не найден"
    except Exception as e:
        return f"Ошибка отправки уведомления: {str(e)}"
