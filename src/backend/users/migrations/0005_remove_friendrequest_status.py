# Generated by Django 5.0.1 on 2024-02-14 07:27

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0004_user_friends_friendrequest_unique_sender_receiver"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="friendrequest",
            name="status",
        ),
    ]