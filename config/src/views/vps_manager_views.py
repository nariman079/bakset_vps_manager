from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response

from src.serializers.vps_manager_serializers import VPSCreateSerializer, VPSStatusEditSerializer
from src.services.vps_manager_services import VPSCreateSrv

class ServerViewSet(ViewSet):
    serializer_class = VPSCreateSerializer
    lookup_field = 'uid'
    
    def create(self, request, *args, **kwargs):
        """Создание сервера"""
        server_data = VPSCreateSerializer(data=request.data)
        server_data.is_valid(raise_exception=True)
        return VPSCreateSrv(serializer_data=server_data.data).execute()

    def list(self, request, *args, **kwargs):
        """Получение списка серверов"""
        return Response()

    def retrieve(self, *args, **kwargs):
        """Получение детальной информации о сервере"""
        return Response()

    @action(methods=['PATCH'], detail=True)
    def change_status(self, request, uid, *args, **kwargs):
        """Изменение данных сервера"""
        server_status = VPSStatusEditSerializer(data=request.data)
        server_status.is_valid(raise_exception=True)
        return Response(data=server_status.data)