import numpy as np

from rest_framework import serializers

from electricity import settings
from electricity.parking.models import ParkingSpot, CameraInput

PARKING_URL = "static/parking{}.png"


class ParkingSpotSerializer(serializers.ModelSerializer):

    class Meta:
        model = ParkingSpot
        fields = ('latitude', 'longitude', 'is_occupied')


class ParkingSerializer(serializers.ModelSerializer):
    image_path = serializers.SerializerMethodField()
    nr_free_spots = serializers.SerializerMethodField()
    nr_occupied_spots = serializers.SerializerMethodField()
    parking_spots = ParkingSpotSerializer(many=True)

    class Meta:
        model = CameraInput
        fields = ('image_path', 'name', 'nr_free_spots', 'nr_occupied_spots', 'parking_spots')

    @staticmethod
    def get_image_path(parking):
        return settings.CURRENT_HOST + 'cameras/{}/snapshot/'.format(parking.id)

    @staticmethod
    def get_nr_free_spots(parking):
        return parking.parking_spots.filter(is_occupied=True).count()

    @staticmethod
    def get_nr_occupied_spots(parking):
        return parking.parking_spots.filter(is_occupied=False).count()

