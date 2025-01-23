import secrets
import string

def generate_password() -> str:
    """Генерация пароля для сервера"""
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(12))