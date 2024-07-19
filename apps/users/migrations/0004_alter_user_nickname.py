# Generated by Django 5.0.7 on 2024-07-19 13:21

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0003_alter_user_nickname_alter_user_username"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="nickname",
            field=models.CharField(
                blank=True, default="User", max_length=20, null=True, unique=True
            ),
        ),
    ]
