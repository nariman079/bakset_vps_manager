# Generated by Django 5.1.5 on 2025-01-24 13:46

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="VPS",
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
                    "uid",
                    models.CharField(
                        max_length=255,
                        unique=True,
                        verbose_name="Уникальный идентификатор",
                    ),
                ),
                (
                    "cpu",
                    models.PositiveIntegerField(
                        editable=False, verbose_name="Количество ядер CPU"
                    ),
                ),
                (
                    "ram",
                    models.FloatField(editable=False, verbose_name="Объем RAM (ГБ)"),
                ),
                (
                    "hdd",
                    models.FloatField(editable=False, verbose_name="Объем HDD (ГБ)"),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("started", "Запущен"),
                            ("blocked", "Заблокирован"),
                            ("stopped", "Остановлен"),
                        ],
                        default="started",
                        max_length=20,
                        verbose_name="Статус сервера",
                    ),
                ),
                (
                    "password",
                    models.CharField(
                        blank=True,
                        editable=False,
                        max_length=100,
                        null=True,
                        verbose_name="Пароль от сервера",
                    ),
                ),
                ("public_ip", models.GenericIPAddressField(editable=False)),
                (
                    "server_os",
                    models.CharField(
                        choices=[("ubuntu:22.04", "Ubuntu v22.04")],
                        default="ubuntu:22.04",
                        max_length=30,
                    ),
                ),
            ],
            options={
                "verbose_name": "Сервер",
                "verbose_name_plural": "Серверы",
                "db_table": "db_vps",
            },
        ),
    ]
