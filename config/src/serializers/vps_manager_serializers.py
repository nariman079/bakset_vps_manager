from rest_framework import serializers

from src.models import VPS

class VPSCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = VPS
        