import numpy as np

from rest_framework import serializers

from electricity.parking.models import ParkingSpot


class ParkingSpotSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParkingSpot
        fields = ('latitude', 'longitude', 'is_occupied')
