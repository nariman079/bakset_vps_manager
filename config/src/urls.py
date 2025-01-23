from django.urls import path, include

from src.views import tour_views
from src.routers import vps_manager_router

urlpatterns = [
    path('api/', include(vps_manager_router.urls))
]

