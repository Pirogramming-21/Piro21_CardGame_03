# Generated by Django 5.0.7 on 2024-07-18 14:44

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
            name="Game",
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
                ("player1_card", models.IntegerField(null=True)),
                ("player2_card", models.IntegerField(null=True)),
                (
                    "status",
                    models.CharField(
                        choices=[("PENDING", "진행중"), ("COMPLETED", "완료")],
                        default="PENDING",
                        max_length=10,
                    ),
                ),
                ("result", models.CharField(max_length=10, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "player1",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="games_as_player1",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "player2",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="games_as_player2",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]