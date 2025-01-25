# Generated by Django 5.1.5 on 2025-01-25 11:32

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("src", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="vps",
            name="status",
            field=models.CharField(
                choices=[
                    ("started", "Запущен"),
                    ("blocked", "Заблокирован"),
                    ("unblocked", "Разблокирован"),
                    ("stopped", "Остановлен"),
                ],
                default="started",
                max_length=20,
                verbose_name="Статус сервера",
            ),
        ),
    ]
