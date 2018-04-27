# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import generics

from electricity.parking.models import ParkingSpot
from electricity.parking.serializers import ParkingSpotSerializer


class ParkingSpotList(generics.ListAPIView):
    serializer_class = ParkingSpotSerializer

    def get_queryset(self):
        return ParkingSpot.objects.all()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
