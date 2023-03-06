from rest_framework import serializers
from .models import Cart


class CartSerializer(serializers.ModelSerializer):    
    def create(self, validated_data):
        return Cart.objects.create(**validated_data)

    class Meta:
        model = Cart
        fields = [
            'id',
            'buyer'
        ]
