# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from electricity.parking.models import CameraInput, ParkingSpot, ParkingLane

admin.site.register(CameraInput)
admin.site.register(ParkingSpot)
admin.site.register(ParkingLane)
