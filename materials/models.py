from django.db import models


class Course(models.Model):
    name = models.CharField(
        max_length=55, verbose_name="Курс", help_text="Укажите курс"
    )
    description = models.TextField(
        verbose_name="Описание курса",
        help_text="Заполните описание",
        blank=True,
        null=True,
    )
    image = models.ImageField(
        upload_to="materials/course_preview",
        verbose_name="Превью курса",
        help_text="Загрузите превью",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"

    def __str__(self):
        return self.name


class Lesson(models.Model):
    name = models.CharField(
        max_length=55, verbose_name="Урок", help_text="Укажите урок"
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="lessons",
        verbose_name="Курс",
        help_text="Укажите курс",
    )
    description = models.TextField(
        verbose_name="Описание урока",
        help_text="Укажите описание урока",
        blank=True,
        null=True,
    )
    image = models.ImageField(
        upload_to="materials/lesson_preview",
        verbose_name="Превью урока",
        help_text="Загрузите превью",
        blank=True,
        null=True,
    )
    video_link = models.URLField(
        max_length=200,
        verbose_name="Ссылка на видео",
        help_text="Укажите ссылку на видео",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"

    def __str__(self):
        return self.name
