# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import generics

from electricity.parking.models import CameraInput
from electricity.parking.serializers import ParkingSerializer


class ParkingSpotList(generics.ListAPIView):
    serializer_class = ParkingSerializer

    def get_queryset(self):
        return CameraInput.objects.all()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


