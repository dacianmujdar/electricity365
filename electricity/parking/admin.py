# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from electricity.parking.models import CameraInput, ParkingSpot, CameraParkingSpot

admin.register(CameraInput)
admin.register(ParkingSpot)
admin.register(CameraParkingSpot)
