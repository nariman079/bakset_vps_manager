from typing import OrderedDict
import uuid
import random
import string
import secrets

import docker
from docker.types import IPAMConfig, IPAMPool
from docker.errors import APIError, NotFound
from rest_framework.response import Response
from rest_framework import status



# get_server_ip('server-f1b9526f-6b38-4c52-9524-8b6ea61898ce')
# stop_server('server-8ef380f0-fa89-410f-b98c-6b110d4ac1d8')
# get_container_status('server-cbf5a26e-fa0e-41e4-bcb6-f49ec0bd88bd')