from rest_framework import serializers


class VPSCreateSerializer(serializers.Serializer):
    hdd = serializers.IntegerField(required=True)
    cpu = serializers.IntegerField(required=True)
    ram = serializers.IntegerField(required=True)
    ssh_key = serializers.CharField(required=False)
    server_password = serializers.CharField(required=False)

class VPSDetailSerializer(serializers.Serializer):
    hdd = serializers.IntegerField()
    cpu = serializers.IntegerField()
    ram = serializers.IntegerField()
    ssh_key = serializers.CharField()
    server_password = serializers.CharField()
    ip_address = serializers.CharField()
    
        