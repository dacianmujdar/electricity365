# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class CameraInput(models.Model):
    url = models.URLField(max_length=200, help_text="The audio stream url")
    name = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True, help_text='True if the audio stream is working')


class CameraParkingSpot(models.Model):
    """
    The information you need to identify the parking spot in video
    """
    video_input = models.ForeignKey('CameraInput', verbose_name='Camera input', related_name='parking_spots')
    upper_right_x = models.IntegerField(verbose_name='Upper Right x')
    upper_right_y = models.IntegerField(verbose_name='Upper Right y')
    bottom_left_x = models.IntegerField(verbose_name='Bottom Left x')
    bottom_right_y = models.IntegerField(verbose_name='Bottom Right y')



class ParkingSpot(models.Model):
    camera_parking_spot = models.OneToOneField(CameraParkingSpot, verbose_name='Camera parking spot',
                                               related_name='parking_spot')
    latitude = models.FloatField()
    longitude = models.FloatField()
