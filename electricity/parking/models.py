# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class CameraInput(models.Model):
    url = models.TextField(help_text="The audio stream url")
    name = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True, help_text='True if the audio stream is working')

    def __unicode__(self):
        return self.name


class ParkingSpot(models.Model):
    """
    The information you need to identify the parking spot in video
    """
    camera = models.ForeignKey('CameraInput', verbose_name='Camera input', related_name='parking_spots')
    center_x = models.IntegerField(verbose_name='Center x')
    center_y = models.IntegerField(verbose_name='Center y')
    width = models.IntegerField(verbose_name='Width')
    height = models.IntegerField(verbose_name='Height')
    rotation_angle = models.IntegerField(default=0, verbose_name='Rotation Angle')

    latitude = models.FloatField()
    longitude = models.FloatField()
    is_occupied = models.BooleanField(default=False)

    def __unicode__(self):
        return "lat {} / lon {} - rect: ({} x {}) - {} - {} - {} from camera {} ".format(self.latitude, self.longitude,
                                                                                         self.center_x, self.center_y,
                                                                                         self.width, self.height,
                                                                                         self.rotation_angle, self.camera)
