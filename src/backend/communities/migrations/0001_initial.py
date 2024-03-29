# Generated by Django 5.0.1 on 2024-01-30 13:55

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Community",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "title",
                    models.CharField(max_length=35, verbose_name="Название сообщества"),
                ),
                (
                    "slug",
                    models.SlugField(
                        max_length=35, unique=True, verbose_name="Псевдоним сообщества"
                    ),
                ),
                (
                    "description",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="Описание сообщества"
                    ),
                ),
                (
                    "avatar",
                    models.ImageField(
                        blank=True,
                        upload_to="community/avatar",
                        verbose_name="Аватар сообщества",
                    ),
                ),
                (
                    "creator",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="creator",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "followers",
                    models.ManyToManyField(
                        blank=True,
                        related_name="followers",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Подписчики",
                    ),
                ),
            ],
            options={
                "verbose_name": "Сообщество",
                "verbose_name_plural": "Сообщества",
                "ordering": ["slug"],
            },
        ),
    ]
