from django.db import models


class VPS(models.Model):
    class Meta:
        db_table = "db_vps"
        verbose_name = "Сервер"
        verbose_name_plural = "Серверы"

    class Status(models.TextChoices):
        STARTED = "started", "Запущен"
        BLOCKED = "blocked", "Заблокирован"
        UNBLOCKED = "unblocked", "Разблокирован"
        STOPPED = "stopped", "Остановлен"

    class ServeOS(models.TextChoices):
        ubuntu_v22_04 = "ubuntu:22.04", "Ubuntu v22.04"
        # @TODO Добавить операционные системы

    uid = models.CharField(
        max_length=255, unique=True, verbose_name="Уникальный идентификатор"
    )
    cpu = models.PositiveIntegerField(
        verbose_name="Количество ядер CPU", editable=False
    )
    ram = models.FloatField(verbose_name="Объем RAM (ГБ)", editable=False)
    hdd = models.FloatField(verbose_name="Объем HDD (ГБ)", editable=False)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default="started",
        verbose_name="Статус сервера",
    )
    password = models.CharField(
        max_length=100,
        editable=False,
        blank=True,
        null=True,
        verbose_name="Пароль от сервера",
    )  # @TODO Сделать отправку пароля на почту
    public_ip = models.GenericIPAddressField(
        max_length=50,
        editable=False,
    )
    server_os = models.CharField(
        max_length=30, choices=ServeOS.choices, default="ubuntu:22.04"
    )

    def __str__(self):
        return f"Сервер {self.uid} (Статус: {self.status})"
