import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models

from .constants import Sex


class User(AbstractUser):
    """Модель пользователя."""

    email = models.EmailField(
        verbose_name="Эл. почта",
        max_length=254,
        unique=True,
    )
    first_name = models.CharField(
        verbose_name="Имя",
        max_length=150,
    )
    last_name = models.CharField(
        verbose_name="Фамилия",
        max_length=150,
    )
    sex = models.TextField(
        verbose_name="Пол",
        choices=Sex,
        blank=True,
    )
    avatar = models.ImageField(
        verbose_name="Аватар",
        upload_to="user/avatar",
        null=True,
        blank=True,
    )
    birth_date = models.DateField(
        verbose_name="Дата рождения",
        null=True,
        blank=True,
    )
    age = models.IntegerField(
        verbose_name="Возраст",
        null=True,
        blank=True,
    )
    biography = models.TextField(
        verbose_name="О себе",
        blank=True,
        max_length=150,
    )
    friends = models.ManyToManyField(
        "User",
        through="Friendship",
        related_name="friends_list",
    )

    @property
    def get_age(self):
        today = datetime.date.today()
        if self.birth_date is not None:
            age = int(
                today.year
                - self.birth_date.year
                - (
                    (today.month, today.day)
                    < (self.birth_date.month, self.birth_date.day)
                )
            )
            return age
        return None

    def save(self, *args, **kwargs):
        self.age = self.get_age
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = [
            "username",
        ]


class FriendRequest(models.Model):
    """Модель запроса в друзья."""

    sender = models.ForeignKey(
        User,
        related_name="requests_sent",
        on_delete=models.CASCADE,
    )
    receiver = models.ForeignKey(
        User,
        related_name="requests_received",
        on_delete=models.CASCADE,
    )
    sent_on = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        verbose_name = "Запрос дружбы"
        verbose_name_plural = "Запросы дружбы"
        ordering = [
            "sent_on",
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["sender", "receiver"],
                name="unique_sender_receiver",
            ),
        ]


class Friendship(models.Model):
    """Модель дружбы между пользователями."""

    another_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="friend",
    )
    current_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="owner",
    )
    friends_from = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        verbose_name = "Друг"
        verbose_name_plural = "Друзья"
        ordering = [
            "friends_from",
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["another_user", "current_user"],
                name="unique_user_another_user",
            ),
        ]
