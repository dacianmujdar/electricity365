# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import math

from rest_framework import generics

from electricity.parking.models import ParkingSpot, CameraInput
from electricity.parking.serializers import ParkingSpotSerializer, ParkingSerializer


def get_bounding_box(latitude_in_degrees, longitude_in_degrees, half_side_in_meters):
    half_side_in_km = half_side_in_meters / 1000
    lat = math.radians(latitude_in_degrees)
    lon = math.radians(longitude_in_degrees)

    radius = 6371
    # Radius of the parallel at given latitude
    parallel_radius = radius*math.cos(lat)

    lat_min = lat - half_side_in_km/radius
    lat_max = lat + half_side_in_km/radius
    lon_min = lon - half_side_in_km/parallel_radius
    lon_max = lon + half_side_in_km/parallel_radius
    rad2deg = math.degrees

    return rad2deg(lat_max), rad2deg(lat_min), rad2deg(lon_max), rad2deg(lon_min)


def nearby_spots(location_latitude, location_longitude, radius):

    bounding_box = get_bounding_box(location_latitude, location_longitude, radius)
    return ParkingSpot.objects.filter(latitude_gte=bounding_box[0], latitude__lte=bounding_box[1],
                                      longitude_gte=bounding_box[2], longitude_lte=bounding_box[3])


class ParkingSpotList(generics.ListAPIView):
    serializer_class = ParkingSerializer

    def get_queryset(self):
        # location_latitude = self.request.GET.get('lat', None)
        # location_longitude = self.request.GET.get('lon', None)
        # radius = self.request.GET.get('radius', None)
        #
        # # if lat, lon and radius are provided - fetch only the parking spots situated nearby
        # if location_latitude and location_longitude and radius:
        #     return nearby_spots(location_latitude, location_longitude, radius)
        # else:
        #     return ParkingSpot.objects.all()
        return CameraInput.objects.all()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


