# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import generics

from electricity.parking.models import ParkingSpot
from electricity.parking.serializers import ParkingSpotSerializer


def nearby_spots(location_latitude, location_longitude, radius):
    return ParkingSpot.objects.all()


class ParkingSpotList(generics.ListAPIView):
    serializer_class = ParkingSpotSerializer

    def get_queryset(self):
        location_latitude = self.request.GET.get('lat', None)
        location_longitude = self.request.GET.get('lon', None)
        radius = self.request.GET.get('radius', None)

        # if lat, lon and radius are provided - fetch only the parking spots situated nearby
        if location_latitude and location_longitude and radius:
            return nearby_spots(location_latitude, location_longitude, radius)
        else:
            return ParkingSpot.objects.all()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
