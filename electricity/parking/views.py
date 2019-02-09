# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime
from PIL import Image, ImageDraw

from django.http import HttpResponse
from rest_framework import generics
from rest_framework import status
from rest_framework.generics import get_object_or_404

from electricity.parking.models import CameraInput
from electricity.parking.serializers import ParkingSerializer
from electricity.predictor.stream_frame_processer import return_frame_from_url, refresh_frames

RED = (245, 10, 10)
GREEN = (0, 255, 0)


class ParkingSpotList(generics.ListAPIView):
    serializer_class = ParkingSerializer

    def get_queryset(self):
        return CameraInput.objects.all()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


def get_parking_snapshot(request, pk):
    # get the camera object
    refresh_frames(1)
    camera = get_object_or_404(CameraInput, id=pk)

    # get the current snapshot
    try:
        image = return_frame_from_url(camera.url)
    except:
        return HttpResponse(status=status.HTTP_502_BAD_GATEWAY)

    request_time = datetime.datetime.now()
    # if (not camera.last_update) or (request_time - camera.last_update).total_seconds() > 15:
    #     return HttpResponse(status=status.HTTP_503_SERVICE_UNAVAILABLE)

    # draw the image
    for camera_parking_spot in camera.parking_spots.all():
        # add coloured rectangle
        upper_left = (camera_parking_spot.upper_right_x, camera_parking_spot.upper_right_y)
        bottom_right = (camera_parking_spot.bottom_left_x, camera_parking_spot.bottom_left_y)

        draw = ImageDraw.Draw(image)
        if camera_parking_spot.is_occupied:
            draw.rectangle((upper_left, bottom_right), outline=RED)
            draw.text(upper_left, camera_parking_spot.code, fill=RED)
        else:
            draw.rectangle((upper_left, bottom_right), outline=GREEN)
            draw.text(upper_left, camera_parking_spot.code, fill=GREEN)
    # get image
    image.save('camera.png')
    return HttpResponse(open('camera.png', 'rb').read(), content_type="image/jpg")
