# Generated by Django 5.0.1 on 2024-02-26 08:40

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0005_remove_friendrequest_status"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="friends",
            field=models.ManyToManyField(
                related_name="friends_list",
                through="users.Friendship",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
