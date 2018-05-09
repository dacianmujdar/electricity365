import numpy as np

from rest_framework import serializers

from electricity.parking.models import ParkingSpot

PARKING_URL = "static/parking{}.png"


class ParkingSpotSerializer(serializers.ModelSerializer):
    camera_image = serializers.SerializerMethodField()

    class Meta:
        model = ParkingSpot
        fields = ('latitude', 'longitude', 'is_occupied', 'camera_image')

    @staticmethod
    def get_camera_image(parking_spot):
        return PARKING_URL.format(parking_spot.camera_parking_spot.camera.id)
