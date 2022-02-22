from .coordinates_serializer import CoordinatesSerializer
from locations.models import Polygon
from rest_framework import serializers


class PolygonSerializer(serializers.ModelSerializer):
    coordinates = CoordinatesSerializer(many=True)

    class Meta:
        model = Polygon
        fields = "__all__"
        extra_kwargs = {"provider": {"required": False}, "id": {"required": False}}

    def to_representation(self, obj):
        representation = super().to_representation(obj)
        representation["provider"] = obj.provider.username
        return representation
