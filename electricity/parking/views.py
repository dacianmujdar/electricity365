# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import math

from rest_framework import generics

from electricity.parking.models import ParkingSpot
from electricity.parking.serializers import ParkingSpotSerializer

r_earth = 6371000.0


def nearby_spots(location_latitude, location_longitude, radius):

    delta_lat = (radius / r_earth) * (180 / math.pi)
    delta_lon = (radius / r_earth) * (180 / math.pi) / math.cos(delta_lat * math.pi / 180)

    max_lat = location_latitude + delta_lat
    min_lat = location_latitude - delta_lat

    max_lon = location_longitude + delta_lon
    min_lon = location_longitude - delta_lon

    return ParkingSpot.objects.filter(latitude_gte=max_lat, latitude__lte=min_lat,
                                      longitude_gte=max_lon, longitude_lte=min_lon)


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


