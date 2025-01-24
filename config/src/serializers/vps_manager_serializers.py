from rest_framework import serializers

from src.utils.vps_manager_utils import get_cpu_count, get_free_disk_space_gb, get_free_virtual_memory
from src.models import VPS

class VPSStatusEditSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=VPS.Status.choices)
    
class VPSCreateSerializer(serializers.Serializer):
    hdd = serializers.IntegerField()
    cpu = serializers.IntegerField()
    ram = serializers.IntegerField()
    ssh_key = serializers.CharField(required=False)
    server_password = serializers.CharField(required=False)

    def validate_hdd(self, value):
        system_free_disk_space = get_free_disk_space_gb()
        if system_free_disk_space < value:
            raise serializers.ValidationError(
                f"Доступно только {system_free_disk_space} памяти в системе"
            )
        return value
    
    def validate_cpu(self, value):
        system_cpu_count = get_cpu_count()
        if system_cpu_count <= value:
            raise serializers.ValidationError(
                f"Доступно только {system_cpu_count} ядер в системе" 
            )
        return value
    
    def validate_ram(self, value):
        system_ram = get_free_virtual_memory()
        if system_ram <= value:
            raise serializers.ValidationError(
                f"Доступно только {system_ram} оперативной памяти в системе"
            )
        return value

class VPSDetailSerializer(serializers.Serializer):
    hdd = serializers.IntegerField()
    cpu = serializers.IntegerField()
    ram = serializers.IntegerField()
    ssh_key = serializers.CharField()
    server_password = serializers.CharField()
    ip_address = serializers.CharField()
    
        
