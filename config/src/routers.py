from rest_framework.routers import SimpleRouter
from src.views.vps_manager_views import ServerViewSet

vps_manager_router = SimpleRouter()
vps_manager_router.register(r'servers', ServerViewSet, basename='servers')


