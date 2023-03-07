from rest_framework import serializers
from .models import User
from adresses.serializers import AddressSerializer


class UserSerializer(serializers.ModelSerializer):
    address = AddressSerializer(read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "password",
            "email",
            "first_name",
            "last_name",
            "photo_url",
            "is_superuser"
            "is_seller"
            "address"
        ]
        extra_kwargs = {
            "password": {"write_only": True},
        }