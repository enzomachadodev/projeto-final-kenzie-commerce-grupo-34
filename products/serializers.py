from rest_framework import serializers

from .models import Product, CartProducts


class ProductSerializer(serializers.ModelSerializer):
    def update(self, instance: Product, validated_data: dict) -> Product:
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()

        return instance

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
            "seller",
        ]
        extra_kwargs = {
            "seller": {"read_only": True},
            "id": {"read_only": True},
        }


class CartProductsSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    total_price = serializers.ReadOnlyField(source="cauculate_total")

    class Meta:
        model = CartProducts
        fields = [
            "product",
            "quantity",
            "total_price",
        ]
        extra_kwargs = {
            "quantity": {"read_only": True},
        }
