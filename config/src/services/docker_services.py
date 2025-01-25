import docker
from docker.errors import NotFound

class ServerManager():

    def __init__(self, server_uid: str):
        self.client = docker.from_env()
        self.server = self.client.containers.get(server_uid)  

    def stop(self) -> None:
        self.server.stop()

    def start(self) -> None:
        self.server.start()
    
    def unlock(self, **kwargs):
        self.server.exec_run("servise ssh start")

    def lock(self):
        # TODO Продумать завершение сессий при блокировке сервера
        self.server.exec_run("servise ssh stop")
        
    @property
    def status(self):
        return self.server.status


def get_server_ip(container_name: str) -> str:
    """Получение IP сервера"""
    client = docker.from_env()
    container = client.containers.get(container_name)
    ip = next(iter(container.attrs["NetworkSettings"]["Networks"].values())).get('IPAddress')
    return ip
