# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import generics

from electricity.parking.models import ParkingSpot
from electricity.parking.serializers import ParkingSpotSerializer


def nearby_spots(location_latitude, location_longitude, radius):
    radius = float(radius) / 1000.0

    query = """SELECT id, (6367*acos(cos(radians(%2f))
                   *cos(radians(latitude))*cos(radians(longitude)-radians(%2f))
                   +sin(radians(%2f))*sin(radians(latitude))))
                   AS distance FROM demo_spot HAVING
                   distance < %2f ORDER BY distance LIMIT 0, %d""" % (
        float(location_latitude),
        float(location_longitude),
        float(location_latitude),
        radius,
        100
    )

    return ParkingSpot.objects.raw(query)


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
