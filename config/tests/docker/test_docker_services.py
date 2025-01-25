import uuid
import random
import time

from django.test import TestCase
import docker


class DockerTestCase(TestCase):
    def setUp(self):
        self.client = docker.from_env()
        self.net_name = f"net-{uuid.uuid4()}"
        self.random_ip = f"{random.randint(1, 254)}.{random.randint(1, 254)}"
        self.network = self.client.networks.create(
            name=self.net_name,
            driver="bridge",
            ipam=docker.types.IPAMConfig(
                pool_configs=[
                    docker.types.IPAMPool(
                        subnet=f"{self.random_ip}.0.0/16",
                        gateway=f"{self.random_ip}.0.1",
                    )
                ]
            ),
        )
        self.server_params = dict(
            image="ubuntu:22.04",
            command="/bin/bash",
            name=str(uuid.uuid4()),
            detach=True,
            tty=True,
            network=self.net_name,
            stdin_open=True,
            ports={
                "22/tcp": random.randint(1000, 9000),
                "7681": random.randint(1000, 9000),
            },
            init=True,
        )
        self.test_container = self.client.containers.create(**self.server_params)

    def test_created_server(self):
        self.assertEqual(self.test_container.status, "created")

    def test_started_server(self):
        self.test_container.start()
        time.sleep(1)
        container_status = self.client.containers.get(self.server_params["name"]).status
        self.assertEqual(container_status, "running")

    def test_stopped_server(self):
        self.test_container.start()
        time.sleep(1)
        self.test_container.stop()
        self.test_container.wait()
        container_status = self.client.containers.get(self.server_params["name"]).status
        self.assertEqual(container_status, "exited")
