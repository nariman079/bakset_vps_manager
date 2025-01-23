from rest_framework import serializers

from src.models import Server

class ServerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Server
        