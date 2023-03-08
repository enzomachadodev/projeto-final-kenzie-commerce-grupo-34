from rest_framework import serializers
from .models import User
from adresses.models import Address
from adresses.serializers import AddressSerializer
from carts.models import Cart
from carts.serializers import CartSerializer
from rest_framework.validators import UniqueValidator
from django.contrib.auth.hashers import make_password


class UserSerializer(serializers.ModelSerializer):
    address = AddressSerializer()
    cart = CartSerializer(read_only=True)

    def create(self, validated_data: dict) -> User:
        address = validated_data.pop("address")
        user = User.objects.create_user(**validated_data)
        Address.objects.create(**address, user=user)
        Cart.objects.create(buyer=user)
        return user

    def update(self, instance: User, validated_data: dict) -> User:
        for key, value in validated_data.items():
            setattr(instance, key, value)
            if key == "password":
                instance.set_password(value)

        instance.save()

        return instance

    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())],
    )

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
            "is_superuser",
            "is_seller",
            "address",
            "cart"
        ]
        extra_kwargs = {
            "password": {"write_only": True},
        }