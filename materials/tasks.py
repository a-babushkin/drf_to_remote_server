from celery import shared_task

from materials.services import check_last_login_and_block, send_update_course


@shared_task
def mail_update_course(pk):
    """Асинхронная рассылка писем пользователям об обновлении материалов курса"""
    send_update_course(pk)


@shared_task
def check_last_login():
    """Проверять пользователей по дате последнего входа и блокировка если не заходил больше месяца"""
    check_last_login_and_block()
