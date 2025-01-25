import psutil
import shutil

import string
import secrets


def get_free_disk_space_gb() -> float:
    """Получение свободного простанства на диске"""
    disk_usage = shutil.disk_usage("/")
    free_disk_space_gb = disk_usage.free / (1024**3)
    return free_disk_space_gb


def get_free_virtual_memory() -> float:
    """Получение свободного пространство в оперативной памяти"""
    memory_info = psutil.virtual_memory()
    free_virtual_memory = memory_info.free / (1024**3)
    return free_virtual_memory


def get_cpu_count(logical: bool = False) -> int:
    """Получение количество ядер или потоков"""
    return psutil.cpu_count(logical=logical)


def generate_password() -> str:
    """Генерация пароля для сервера"""
    alphabet = string.ascii_letters + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(12))
