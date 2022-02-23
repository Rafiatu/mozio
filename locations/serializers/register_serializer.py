from rest_framework import serializers
from locations.models import Provider
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True, validators=[UniqueValidator(queryset=Provider.objects.all())]
    )

    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )

    class Meta:
        model = Provider
        fields = (
            "username",
            "password",
            "email",
            "first_name",
            "last_name",
            "phone_number",
            "language",
            "currency",
        )
        extra_kwargs = {
            "first_name": {"required": True},
            "last_name": {"required": True},
        }

    def create(self, validated_data):
        password = validated_data["password"]
        del validated_data["password"]
        user = Provider.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user
