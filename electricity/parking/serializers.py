import numpy as np

from rest_framework import serializers

from electricity.parking.models import ParkingSpot


class ParkingSpotSerializer(serializers.ModelSerializer):
    is_occupied = serializers.SerializerMethodField()

    class Meta:
        model = ParkingSpot
        fields = ('latitude', 'longitude', 'is_occupied')

    def get_is_occupied(self, instance):
        return np.random.rand() > .5
