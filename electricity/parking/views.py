# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import Http404
from django.http import HttpResponse
from rest_framework import generics
from rest_framework.generics import get_object_or_404

from electricity.parking.models import CameraInput
from electricity.parking.serializers import ParkingSerializer
from electricity.predictor.stream_frame_processer import refresh_frames, SNAPSHOT_LOCATION
from PIL import Image, ImageDraw

RED = (245, 10, 10)
GREEN = (0, 255, 0)


class ParkingSpotList(generics.ListAPIView):
    serializer_class = ParkingSerializer

    def get_queryset(self):
        return CameraInput.objects.all()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


def get_parking_snapshot(request, pk):
    get_object_or_404(CameraInput, id=pk)
    try:
        response = HttpResponse(open(SNAPSHOT_LOCATION.format(pk), 'rb').read(), content_type="image/png")
    except:
        raise Http404
    return response
