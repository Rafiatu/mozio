from rest_framework import serializers
from locations.models import Coordinate


class CoordinatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coordinate
        fields = "__all__"

    def to_representation(self, obj):
        return [obj.latitude, obj.longitude]
