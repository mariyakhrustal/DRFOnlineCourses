from decimal import Decimal

from django.core.management.base import BaseCommand

from materials.models import Course, Lesson
from users.models import Payment, User


class Command(BaseCommand):
    help = "Add test payments to the database"

    def handle(self, *args, **kwargs):

        user, created = User.objects.get_or_create(
            email="test@example.com",
            defaults={"password": "12345", "city": "Test City"},
        )
        if created:
            self.stdout.write(self.style.SUCCESS("Создан тестовый пользователь."))
        else:
            self.stdout.write(
                self.style.WARNING("Тестовый пользователь уже существует.")
            )

        course, created = Course.objects.get_or_create(
            name="Тестовый курс", defaults={"description": "Описание тестового курса"}
        )
        if created:
            self.stdout.write(self.style.SUCCESS("Создан тестовый курс."))
        else:
            self.stdout.write(self.style.WARNING("Тестовый курс уже существует."))

        lesson, created = Lesson.objects.get_or_create(
            name="Тестовый урок",
            defaults={"description": "Описание тестового урока", "course": course},
        )
        if created:
            self.stdout.write(self.style.SUCCESS("Создан тестовый урок."))
        else:
            self.stdout.write(self.style.WARNING("Тестовый урок уже существует."))

        payment1, created = Payment.objects.get_or_create(
            user=user,
            course=course,
            defaults={"payment_amount": Decimal("12000.00"), "payment_method": "cash"},
        )
        if created:
            self.stdout.write(self.style.SUCCESS("Создан платёж за курс."))
        else:
            self.stdout.write(self.style.WARNING("Платёж за курс уже существует."))

        payment2, created = Payment.objects.get_or_create(
            user=user, lesson=lesson, defaults={"payment_amount": Decimal("3500.00")}
        )
        if created:
            self.stdout.write(self.style.SUCCESS("Создан платёж за урок."))
        else:
            self.stdout.write(self.style.WARNING("Платёж за урок уже существует."))

        self.stdout.write("Таблица платежей загружена.")
