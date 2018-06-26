# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class CameraInput(models.Model):
    url = models.TextField(help_text="The audio stream url")
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class ParkingSpot(models.Model):
    """
    The information you need to identify the parking spot in video
    """
    camera = models.ForeignKey('CameraInput', verbose_name='Camera input', related_name='parking_spots')
    code = models.CharField(max_length=300, help_text='Identifier provided by the parking admin')

    # image localization
    upper_right_x = models.IntegerField(verbose_name='Upper Right x')
    upper_right_y = models.IntegerField(verbose_name='Upper Right y')
    bottom_left_x = models.IntegerField(verbose_name='Bottom Left x')
    bottom_left_y = models.IntegerField(verbose_name='Bottom Right y')

    # map localization
    latitude = models.FloatField()
    longitude = models.FloatField()

    is_occupied = models.BooleanField(default=False)

    def __str__(self):
        return "{} - lat {} / lon {} - rect: [{} x {}] - [{} x {}] - from camera {} ".format(self.code, self.latitude, self.longitude,
                                                                                             self.upper_right_x, self.upper_right_y,
                                                                                             self.bottom_left_x, self.bottom_right_y,
                                                                                             self.camera)
