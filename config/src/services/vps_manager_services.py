from typing import OrderedDict
import uuid
import random

import docker
from docker.errors import APIError
from rest_framework.response import Response
from rest_framework import status

from src.utils.vps_manager_utils import generate_password

NETWORK_NAME = 'vps_servers'
IMAGE_NAME = "ubuntu:22.04"

unique_ports = set()
unique_ips = set()

def get_ip() -> str:
    """Получение IP для сервера"""
    while True:
        ip = f"{random.randint(0, 254)}.{random.randint(0, 254)}"
        if ip not in unique_ips:
            unique_ips.add(ip)
            return ip

def remove_ip(ip) -> int:
    """Освобождение IP"""
    if ip in unique_ips:
        unique_ips.remove(ip)

def get_port() -> int:
    """Получение порта для сервера"""
    while True:
        port = random.randint(10000, 60000)
        if port not in unique_ports:
            unique_ports.add(port)
            return port

def remove_port(port) -> int:
    """Освобождение порта"""
    if port in unique_ports:
        unique_ports.remove(port)


class VPSCreateSrv:
    """Создание сервера"""
    def __init__(self, serializer_data: OrderedDict) -> None:
        self.client = docker.from_env()
        self.hdd = serializer_data['hdd']
        self.cpu = serializer_data['cpu']
        self.ram = serializer_data['ram']

        self.ssh_key = serializer_data.get('ssh_key')
        self.server_password = serializer_data.get('password', generate_password())
        self.container_name = "server-" + str(uuid.uuid4())
  

    def _create_network(self) -> None:
        """Создание сети для сервера"""
        self.network_name = f"{NETWORK_NAME}-{uuid.uuid4()}"

        ip = get_ip()

        self.network = self.client.networks.create(
            name=self.network_name,
            driver='bridge',
            ipam=docker.types.IPAMConfig(
            pool_configs=[
                docker.types.IPAMPool(
                    subnet=f"{ip}.0.0/16",
                    gateway=f"{ip}.0.1"
                )
            ]
        )
    )
    
    def _create_server_params(self) -> None:
        """Подготовка команд для запуска Сервера"""
        if not self.network:
            raise ValueError("Сеть Docker не настроена")

        command_list  = [
            "apt update && apt upgrade -y && ",
            "apt-get update && apt-get install -y systemd && apt-get clean",
            f"echo 'root:{self.server_password}' | chpasswd && ",
            "apt install -y openssh-server && ",
            'sed -i "s/#PermitRootLogin prohibit-password/PermitRootLogin yes/" /etc/ssh/sshd_config && ',
            "service ssh restart && ",
        ]
        
        if self.ssh_key:
            command_list.extend(
                [
                    
                    "chmod 600 /root/.ssh/authorized_keys &&",
                    f"echo '{self.ssh_key}' >> /root/.ssh/authorized_keys &&",
                ]
            )
        command_list.append("/bin/bash")
        print(command_list)
        environment = [
            'DEBIAN_FRONTEND=noninteractive',
            'TZ=Europe/Moscow'
        ]
        self.server_params = dict(
            environment=environment,
            image=IMAGE_NAME,
            command=f"bash -c '{''.join(command_list)}'",
            name=self.container_name,
            detach=True,
            tty=True,
            network=NETWORK_NAME,  
            stdin_open=True,
            ports={'22/tcp': get_port()},
            init=True
        )
    
    def _create_server(self):
        """Создание сервера(контейнера)"""
        try:
            self.server = self.client.containers.run(**self.server_params)
        except APIError as ex:
            return Response(exception=ex)
    

    def execute(self):
        
        self._create_network()
        self._create_server_params()
        self._create_server()
        network_settings = next(iter(self.server.attrs["NetworkSettings"]["Networks"].values()))
        ip_address = network_settings["IPAddress"]

        return Response(
            status=status.HTTP_201_CREATED,
            data={
                "ip":ip_address,
                'password': self.server_password,
                'networks': network_settings,
                'server': self.server_params
            }
        )
