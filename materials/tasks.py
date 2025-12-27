from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

from materials.models import Subscription


@shared_task
def example():
    print("hello world")


@shared_task
def send_update_course_email(course_id, course_name):
    subscriptions = Subscription.objects.filter(course=course_id)
    email_list = [sub.user.email for sub in subscriptions]
    if email_list:
        send_mail(
            subject=f"Обновление курса: {course_name}",
            message=f"Здравствуйте! В курсе '{course_name}' произошли изменения. Зайдите на платформу, чтобы проверить новые материалы.",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=email_list,
            fail_silently=False,
        )
