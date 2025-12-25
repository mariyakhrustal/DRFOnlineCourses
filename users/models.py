from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = None

    email = models.EmailField(
        unique=True, verbose_name="Почта", help_text="Укажите почту"
    )
    phone = models.CharField(
        max_length=35,
        blank=True,
        null=True,
        verbose_name="Телефон",
        help_text="Укажите телефон",
    )
    city = models.CharField(
        max_length=55,
        blank=True,
        null=True,
        verbose_name="Город",
        help_text="Укажите город",
    )
    avatar = models.ImageField(
        upload_to="users/avatars",
        blank=True,
        null=True,
        verbose_name="Аватар",
        help_text="Загрузите аватар",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Payment(models.Model):
    CASH = "cash"
    TRANSFER = "transfer"

    PAYMENT_METHOD_CHOICES = [
        (CASH, "Наличные"),
        (TRANSFER, "Перевод на счёт"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="payments",
        verbose_name="Пользователь",
        help_text="Укажите пользователя",
    )
    date = models.DateField(
        blank=True,
        null=True,
        verbose_name="Дата платежа",
        help_text="Укажите дату платежа",
    )
    course = models.ForeignKey(
        "materials.Course",
        on_delete=models.CASCADE,
        related_name="payments",
        blank=True,
        null=True,
        verbose_name="Оплаченный курс",
        help_text="Укажите оплаченный курс",
    )
    lesson = models.ForeignKey(
        "materials.Lesson",
        on_delete=models.CASCADE,
        related_name="payments",
        blank=True,
        null=True,
        verbose_name="Оплаченный урок",
        help_text="Укажите оплаченный урок",
    )
    amount = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name="Сумма платежа",
        help_text="Укажите сумму платежа",
    )
    method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        default=TRANSFER,
        blank=True,
        null=True,
        verbose_name="Способ оплаты",
        help_text="Укажите способ оплаты",
    )
    session_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Id на сессии",
        help_text="Укажите id на сессии",
    )
    session_url = models.URLField(
        max_length=400,
        blank=True,
        null=True,
        verbose_name="Ссылка на оплату",
        help_text="Укажите ссылку на оплату",
    )

    def __str__(self):
        return self.amount

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"
