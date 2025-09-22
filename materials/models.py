from django.db import models

from users.models import User


# ===== Секция курсов ===============================================
class Course(models.Model):
    """Описание модели Курса"""

    title = models.CharField(
        max_length=250, verbose_name="наименование", help_text="Введите название курса"
    )
    description = models.TextField(
        verbose_name="описание",
        blank=True,
        null=True,
        help_text="Введите описание курса",
    )
    image = models.ImageField(
        verbose_name="изображение",
        blank=True,
        null=True,
        help_text="Загрузите изображение курса",
        upload_to="uploads/",
    )
    price = models.PositiveIntegerField(
        default=1000, blank=True, null=True, verbose_name="Цена курса"
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        related_name="course",
        verbose_name="Владелец",
    )

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"
        ordering = ["title"]


# ===== Секция уроков ===============================================
class Lesson(models.Model):
    """Описание модели Урока"""

    title = models.CharField(
        max_length=250, verbose_name="наименование", help_text="Введите название урока"
    )
    description = models.TextField(
        verbose_name="описание",
        blank=True,
        null=True,
        help_text="Введите описание курса",
    )
    image = models.ImageField(
        verbose_name="изображение",
        blank=True,
        null=True,
        help_text="Загрузите изображение курса",
        upload_to="uploads/",
    )
    video = models.CharField(
        verbose_name="ссылка на видео",
        blank=True,
        null=True,
        help_text="Введите ссылку на видео курса",
    )
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, verbose_name="курс", related_name="lessons"
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        related_name="lesson",
        verbose_name="Владелец",
    )

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
        ordering = ["title"]


# ===== Секция подписок ===============================================
class Subscription(models.Model):
    """Описание модели Подписка"""

    subscripted = models.BooleanField(
        verbose_name="Подписка",
        blank=True,
        null=True,
        help_text="Подписка на курс",
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        null=True,
        related_name="subscription_course",
        verbose_name="Подписанный курс",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        related_name="subscription_user",
        verbose_name="Пользователь",
    )

    def __str__(self):
        return f"{self.user.email} subscribed to {self.course.title}"

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
        ordering = ["course__title"]
        unique_together = ("user", "course")
