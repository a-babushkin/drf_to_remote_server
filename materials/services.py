import logging
import os
from datetime import datetime, timedelta, timezone

from django.core.mail import send_mail
# from django.utils import timezone

from config import settings
from materials.models import Course, Subscription
from users.models import User

logger = logging.getLogger(__name__)
log_file_path = os.path.join(settings.BASE_DIR, "logs", "mailing_send.log")
file_handler = logging.FileHandler(log_file_path, encoding="utf-8")
formatter = logging.Formatter("%(asctime)s [%(levelname)s]: %(message)s")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)


def send_update_course(pk):
    """Отправка рассылки по требованию"""
    course_subscriptions = Subscription.objects.filter(course=pk)
    course_title = Course.objects.filter(id=pk).first().title

    from_email = settings.EMAIL_HOST_USER
    subject = "Обновление курса"
    message = f"Курс {course_title} обновлен."

    for subscription in course_subscriptions:
        if not subscription.user.email:
            logger.warning(
                f"У получателя {subscription} отсутствует действительный адрес электронной почты."
            )
            break
        try:
            send_mail(subject, message, from_email, [subscription.user.email])
            logger.info(
                f"На почту: {subscription.user.email} отправлено письмо про обновление курса: {course_title}."
            )

        except Exception as e:
            logger.error(f"Ошибка отправки: {e}")


def check_last_login_and_block():
    """
    Проверка последнего входа пользователей и отключение неактивных пользователей.
    Если пользователь не заходил более 30 дней, его аккаунт деактивируется.
    """
    users = User.objects.exclude(last_login__isnull=True)
    now = datetime.now(timezone.utc)  # Правильно объявляем текущее время в UTC
    today = now.date()

    for user in users:
        # Приводим последнее время входа к UTC
        last_login_in_utc = user.last_login.astimezone(timezone.utc)

        # Вычисляем разницу в днях
        delta = today - last_login_in_utc.date()

        if delta.days > 30:
            user.is_active = False
            user.save()
            print(f"Пользователь {user.email} не входил больше месяца и отключён.")
        else:
            print("Пользователь активен.")