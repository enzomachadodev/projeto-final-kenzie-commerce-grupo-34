from rest_framework import serializers
from .models import Cart
from products.models import Product
from products.serializers import ProductSerializer


class CartSerializer(serializers.ModelSerializer):
    products = ProductSerializer(read_only=True, many=True)

    class Meta:
        model = Cart
        fields = [
            'id',
            'buyer',
            "products"
        ]
