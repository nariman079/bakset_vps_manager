from django.db import models

class VPS(models.Model):

    class Meta:
        db_table = 'db_vps'
        verbose_name = "Сервер"
        verbose_name_plural = "Серверы"

    class Status(models.TextChoices):
        STARTED = 'started', 'Запущен'
        BLOCKED = 'blocked', 'Заблокирован'
        STOPPED = 'stopped', 'Остановлен'

    uid = models.CharField(
        max_length=255, 
        unique=True, 
        verbose_name="Уникальный идентификатор"
    )
    cpu = models.PositiveIntegerField(
        verbose_name="Количество ядер CPU",
        editable=False
    )
    ram = models.PositiveIntegerField(
        verbose_name="Объем RAM (ГБ)",
        editable=False
    )
    hdd = models.PositiveIntegerField(
        verbose_name="Объем HDD (ГБ)",
        editable=False
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default='started',
        verbose_name="Статус сервера"
    )
    server_password = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Пароль от сервера"
    )

    def __str__(self):
        return f"Сервер {self.uid} (Статус: {self.status})"

    
