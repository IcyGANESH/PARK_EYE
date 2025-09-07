from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.utils.timezone import now
from django.shortcuts import get_object_or_404

from PARK_EYE.models import Suspected, Police, VehicleRecord, Location
from .serializers import (
    SuspectedSerializer,
    PoliceSerializer,
    VehicleRecordSerializer,
    LocationSerializer
)

# ------------------ MODEL VIEWSETS ------------------

class SuspectedViewSet(viewsets.ModelViewSet):
    queryset = Suspected.objects.all().order_by('-date_time')
    serializer_class = SuspectedSerializer


class VehicleRecordViewSet(viewsets.ModelViewSet):
    queryset = VehicleRecord.objects.all().order_by('-in_date_time')
    serializer_class = VehicleRecordSerializer


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer


class PoliceViewSet(viewsets.ModelViewSet):
    queryset = Police.objects.all()
    serializer_class = PoliceSerializer


# ------------------ CUSTOM API ENDPOINTS ------------------

@api_view(["POST"])
def add_suspected_vehicle(request):
    """
    API to add a suspected vehicle
    """
    serializer = SuspectedSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(date_time=now(), is_founded=False)
        return Response({"message": "Suspected vehicle added successfully", "data": serializer.data},
                        status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def police_login_check(request):
    """
    API for police login authentication
    """
    username = request.data.get("username")
    password = request.data.get("password")

    try:
        police = Police.objects.get(username=username)
        if police.check_password(password):
            return Response({
                "message": "Login successful",
                "police_id": police.id,
                "username": police.username,
                "locations": list(police.locations.values_list("name", flat=True))
            }, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid username or password"}, status=status.HTTP_401_UNAUTHORIZED)
    except Police.DoesNotExist:
        return Response({"error": "Invalid username or password"}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(["GET"])
def police_dashboard(request, police_id):
    """
    API for police dashboard - fetch suspected vehicles in police assigned locations
    """
    police = get_object_or_404(Police, id=police_id)
    police_locations = police.locations.values_list("name", flat=True)

    suspected_vehicles = Suspected.objects.filter(found_location__in=police_locations)
    serializer = SuspectedSerializer(suspected_vehicles, many=True)

    return Response({
        "police": {
            "id": police.id,
            "username": police.username,
            "locations": list(police_locations)
        },
        "suspected_vehicles": serializer.data
    }, status=status.HTTP_200_OK)
