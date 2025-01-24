import docker
from docker.errors import NotFound

class ServerManager():
    def __init__(self, server: str):
        self.client = docker.from_env()
        try:
            self.server = self.client.containers.get(container_name)
        except NotFound as ex:
            raise ValueError(f"Такой контейнер не найден: {ex}")
    
    def stop(self) -> None:
        self.server.stop()

    def start(self) -> None:
        self.server.start()
    
    def unlock(self):
        self.server.exec_run("")

    def lock(self):
        self.server.exec_run("")
    

def stop_server(container_name: str) -> None:
    """Остановка сервера"""
    client = docker.from_env()
    container = client.containers.get(container_name)
    container.stop()

def lock_server(container_name: str) -> None:
    """Блокировка сервера"""
    client = docker.from_env()
    container = client.containers.get(container_name)
    container.exec_run('service ssh stop')
    container.stop()
    container.start()

def unlock_server(container_name: str) -> None:
    """Разблокировка сервера"""
    client = docker.from_env()
    container = client.containers.get(container_name)
    container.exec_run("service ssh start")

def get_container_status(container_name) -> str | None:
    """Получение статуса сервера"""
    try:
        client = docker.from_env()
        container = client.containers.get(container_name)
        return container.status
    except docker.errors.NotFound:
        return None
    except docker.errors.APIError as e:
        raise ValueError(f"Ошибка API {str(e)}")

def get_server_ip(container_name: str) -> str:
    """Получение IP сервера"""
    client = docker.from_env()
    container = client.containers.get(container_name)
    ip = next(iter(container.attrs["NetworkSettings"]["Networks"].values())).get('IPAddress')
    return ip
