from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action

from src.serializers.vps_manager_serializers import VPSCreateSerializer

class ServerViewSet(ViewSet):
    authentication_classes = None


    @action(methods=['POST'], detail=False)
    def create_server(self, request, *args, **kwargs):
        """Создание сервера"""
        pass
    
    @action(methods=['PATCH'], detail=False)
    def edit_server(self, request, *args, **kwargs):
        """Изменение данных сервера"""
        pass

    @action(methods=['GET'], detail=False)
    def get_server_list(self, request, *args, **kwargs):
        """Получение списка серверов"""
        pass

    @action(methods=['GET'], detail=True)
    def get_server_detail(self, uid: str, *args, **kwargs):
        """Получение детальной информации о сервере"""
        pass

    

    