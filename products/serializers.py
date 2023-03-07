from rest_framework import serializers

from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "image_url",
            "price",
            "description",
            "category",
            "stock",
            "seller_id",
        ]
