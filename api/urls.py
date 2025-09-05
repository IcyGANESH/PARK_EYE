from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    SuspectedViewSet, VehicleRecordViewSet,
    LocationViewSet, PoliceViewSet,
    add_suspected_vehicle, police_login_check, police_dashboard
)

router = DefaultRouter()
router.register(r'suspected', SuspectedViewSet)
router.register(r'vehicles', VehicleRecordViewSet)
router.register(r'locations', LocationViewSet)
router.register(r'police', PoliceViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('add-suspected/', add_suspected_vehicle, name="add_suspected"),
    path('police-login/', police_login_check, name="police_login"),
    path('police-dashboard/<int:police_id>/', police_dashboard, name="police_dashboard"),
]
