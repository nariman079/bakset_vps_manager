from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from django.core.exceptions import FieldError

from src.serializers.vps_manager_serializers import VPSCreateSerializer, VPSStatusEditSerializer, VPSDetailSerializer
from src.services.vps_manager_services import VPSCreateSrv, VPSStatusEditSrv, get_vps_srv
from src.models import VPS

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
        try:
            query = {k:v for k,v in self.request.query_params.items()}
            queryset = VPS.objects.filter(**query)
            vps_list = VPSDetailSerializer(instance=queryset, many=True)
        except FieldError as ex:
            return Response(data={
                'message': "Ошибка полей, проверьте query params",
                'detail': str(ex)
            })
        print(self.request.query_params)
        return Response(vps_list.data)

    def retrieve(self, *args, **kwargs):
        """Получение детальной информации о сервере"""
        if uid := kwargs.get('uid'):
            return get_vps_srv(uid=uid)
        return Response(
            status=400,
            data={
                "Произошла ошибка"
            }
        )

    @action(methods=['PATCH'], detail=True)
    def change_status(self, request, uid, *args, **kwargs):
        """Изменение данных сервера"""
        server_status = VPSStatusEditSerializer(data=request.data)
        server_status.is_valid(raise_exception=True)
        return VPSStatusEditSrv(uid, server_status.data).execute()