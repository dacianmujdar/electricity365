# -*- coding: utf-8 -*-
from __future__ import unicode_literals, division

from django.db import models
import math


class CameraInput(models.Model):
    url = models.TextField(help_text="The audio stream url")
    name = models.CharField(max_length=200)
    last_update = models.DateTimeField(null=True, blank=True)

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
                                                                                             self.bottom_left_x, self.bottom_left_y,
                                                                                             self.camera)


class ParkingLane(models.Model):
    """
    A parking lane with multiple possible parking spots
    """
    camera = models.ForeignKey('CameraInput', verbose_name='Camera input', related_name='parking_lanes')
    code = models.CharField(max_length=300, help_text='Identifier provided by the parking admin')

    # median line
    left_x_up = models.IntegerField(verbose_name='Median line x left UP')
    left_y_up = models.IntegerField(verbose_name='Median line y left UP')
    right_x_up = models.IntegerField(verbose_name='Median line x right UP')
    right_y_up = models.IntegerField(verbose_name='Median line y right UP')

    left_x_down = models.IntegerField(verbose_name='Median line x left DOWN')
    left_y_down = models.IntegerField(verbose_name='Median line y left DOWN')
    right_x_down = models.IntegerField(verbose_name='Median line x right DOWN')
    right_y_down = models.IntegerField(verbose_name='Median line y right DOWN')

    left_width = models.IntegerField(verbose_name='Width of left rectangle')
    right_width = models.IntegerField(verbose_name='Width of right rectangle')

    @property
    def dx_up(self):
        return abs(self.right_x_up - self.left_x_up)

    @property
    def dy_up(self):
        return abs(self.right_y_up - self.left_y_up)

    @property
    def dx_down(self):
        return abs(self.right_x_down - self.left_x_down)

    @property
    def dy_down(self):
        return abs(self.right_y_down - self.left_y_down)

    def get_distance_up(self):
        return int(math.sqrt(self.dx_up * self.dx_up + self.dy_up * self.dy_up))

    def get_distance_down(self):
        return int(math.sqrt(self.dx_down * self.dx_down + self.dy_down * self.dy_down))

    def get_point_at_distance_ratio_up(self, distance_ratio):
        x = (1 - distance_ratio) * int(self.left_x_up) + distance_ratio * self.right_x_up
        y = (1 - distance_ratio) * int(self.left_y_up) + distance_ratio * self.right_y_up
        return int(x), int(y)

    def get_point_at_distance_ratio_down(self, distance_ratio):
        x = (1 - distance_ratio) * int(self.left_x_down) + distance_ratio * self.right_x_down
        y = (1 - distance_ratio) * int(self.left_y_down) + distance_ratio * self.right_y_down
        return int(x), int(y)

