
import docker
import pprint
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

        self.server.exec_run("servise ssh stop")
        self.server.stop()
        self.server.start()
        if password := kwargs.get('password'):
            self.server.exec_run(
                cmd=f"ttyd --credential root:{password} --writable -p 7681 bash"
            )

    def lock(self):
        self.server.exec_run("service ssh start")
    
    @property
    def status(self):
        return self.server.status

container_id = "ab344cbf-9fab-4737-9d4c-f4cca861222f"
manage = ServerManager(container_id)
pprint.pprint(manage.server.attrs)