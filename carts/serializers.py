from rest_framework import serializers
from .models import Cart
from products.models import Product
from products.serializers import ProductSerializer, CartProductsSerializer


class CartSerializer(serializers.ModelSerializer):
    cart_products_pivo = CartProductsSerializer(read_only=True, many=True)
    cart_total = serializers.ReadOnlyField(source="cauculate_total")

    class Meta:
        model = Cart
        fields = [
            "id",
            "cart_products_pivo",
            "cart_total",
        ]
