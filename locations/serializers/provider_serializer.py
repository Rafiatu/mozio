from rest_framework import serializers
from locations.models import Provider


class ProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provider
        fields = ["username", "email", "phone_number", "language", "currency"]
