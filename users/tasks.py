from datetime import timedelta

from celery import shared_task
from django.utils import timezone

from users.models import User


@shared_task
def block_inactive_users():
    today = timezone.now()
    month_ago = today - timedelta(days=30)
    users = User.objects.filter(last_login__isnull=False, is_active=True)
    for user in users:
        if user.last_login < month_ago:
            user.is_active = False
            print(f"Пользователь {user.email} больше не активен")
            user.save()
