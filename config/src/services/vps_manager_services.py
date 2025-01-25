from typing import OrderedDict
import uuid
import random

import docker
from docker.errors import APIError, NotFound
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import status

from src.models import VPS
from src.services.docker_services import ServerManager, get_server_ip
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
        self.server_password = serializer_data.get('server_password', generate_password())
        self.container_name =  str(uuid.uuid4())
  

    def _create_network(self) -> None:
        """Создание сети для сервера"""
        self.network_name = f"{NETWORK_NAME}-{uuid.uuid4()}"

        ip = get_ip()
        self.ip_address = f"{ip}.0.2"
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

        self.command_list  = [
            "apt update", "apt upgrade -y",
            "apt-get update ",
            "apt-get install -y systemd",
            "apt-get install -y wget",
            "apt-get clean",
            f"echo 'root:{self.server_password}' | chpasswd",
            "apt install -y openssh-server",
            'sed -i \'s|#PermitRootLogin prohibit-password|PermitRootLogin yes|\' /etc/ssh/sshd_config',
            "service ssh restart",
        ]
        
        if self.ssh_key:
            self.command_list.extend(
                [
                    "chmod 600 /root/.ssh/authorized_keys",
                    f"echo '{self.ssh_key}' >> /root/.ssh/authorized_keys",
                ]
            )
        
        self.command_list.append(f"ttyd --credential root:{self.server_password} --writable -p 7681 bash")
        environment = [
            'DEBIAN_FRONTEND=noninteractive',
            'TZ=Europe/Moscow'
        ]
        self.server_params = dict(
            environment=environment,
            image=IMAGE_NAME,
            command='/bin/bash',
            name=self.container_name,
            detach=True,
            tty=True,
            network=self.network_name,  
            stdin_open=True,
            ports={'22/tcp': get_port(), '7681': get_port()},
            init=True
        )
    
    def _create_server(self):
        """Создание сервера(контейнера)"""
        try:
            self.server = self.client.containers.run(**self.server_params)
            
            comma = self.server.exec_run(
                f'sh -c "{" && ".join(self.command_list)}" ', 
                user='root', 
                detach=True
            )
            self.server.exec_run(
                f"",
                user="root",
                detach=True
            )
            
        except APIError as ex:
            return Response(exception=ex)
    
    def _create_vps(self):
        """Создание VPS в Базе"""
        try:
            VPS.objects.create(
                uid=self.container_name,
                cpu=self.cpu,
                hdd=self.hdd,
                ram=self.ram,
                password=self.server_password,
                public_ip=self.ip_address           
            )
        except Exception as ex:
            raise ValidationError(str(ex))

    def execute(self):
        self._create_network()
        self._create_server_params()
        self._create_server()
        self._create_vps()
        self.server_params.pop('command')
        return Response(
            status=status.HTTP_201_CREATED,
            data={
                "message":"Сервер создается и будет готов к работе через 60-90 секунд",
                "data":{
                    "ip":self.ip_address,
                    'terminal_url': f"http://{self.ip_address}:7681/",
                    'command_for_connect': f"ssh root@{self.ip_address}",
                    'password': self.server_password,
                    'server': self.server_params,
                }
            }
        )

class VPSStatusEditSrv:
    def __init__(
        self, 
        uid: str,
        serializer_data: OrderedDict
    ) -> None:
        self.uid = uid
        self.new_status = serializer_data['status']
        
        try:
            self.manager = ServerManager(server_uid=self.uid)
        except NotFound:
            raise ValidationError(detail={"uid": "Такого сервера нет в системе"})
        
    def _get_vps_object(self) -> None: 
        """Получение объекта из базы данных"""
        self.vps_object = VPS.objects.filter(uid=self.uid).first()
        if not self.vps_object:
            raise ValidationError(detail={"uid": "Такого сервера нет в базе"})

    def _get_and_change_server_status(self) -> None: 
        """Изменение статуса сервера"""
        
        match self.new_status:
            case 'started':
                self.manager.start()
            case 'blocked':
                self.manager.lock()
            case 'unblocked':
                self.manager.unlock()
            case 'stopped':
                self.manager.stop()

        self.vps_object.status = self.new_status
        self.vps_object.save()

        return Response(
            status=200,
            data={
                "message": f"Изменение статуса сервера на {self.vps_object.get_status_display()}"
            }
        )
    
    def execute(self) -> Response: 
        self._get_vps_object()
        return self._get_and_change_server_status()


def get_vps_srv(uid: str) -> Response:
    vps = VPS.objects.filter(uid=uid).values(
        'uid',
        'cpu',
        'ram',
        'hdd',
        'status',
        'password',
        'public_ip',
        'server_os'
    ).first()

    if not vps:
        return Response(
            status=404,
            data={
                "message": "Такого сервера нет в системе"
            }
        )
    
    return Response(data=vps)

