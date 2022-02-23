from rest_framework import serializers
from locations.models import Provider


class ProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provider
        fields = ["id", "username", "email", "phone_number", "language", "currency"]
        extra_kwargs = {"id": {"required": False}}
