from rest_framework import serializers

from .models import Order

# from products.serializers import ProductSerializer


class OrderSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        return Order.objects.create(**validated_data)

    buyer = serializers.CharField(
        max_length=40, source="buyer.first_name", read_only=True
    )
    # products = ProductSerializer(many=True, source='ordered_products', read_only=True)

    class Meta:
        model = Order
        fields = ["id", "status", "created_at", "buyer"]
        # fields = ["id", "status", "created_at", "buyer", "products"]
        read_only_fields = ["id", "buyer"]
        # read_only_fields = ["id", "buyer", "products"]
