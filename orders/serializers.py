from rest_framework import serializers

from .models import Order
from products.serializers import ProductSerializer


class OrderSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        cart = validated_data.pop("cart")

        order = Order.objects.create(
            **validated_data
        )

        # import ipdb
        # ipdb.set_trace()

        order.ordered_products.set(cart.products.all())
        order.save()
        return order

    def update(self, instance: Order, validated_data: dict) -> Order:
        if validated_data.get("status"):
            instance["status"] = validated_data["status"]
            instance.save()
        return instance

    buyer = serializers.CharField(
        max_length=40, source="buyer.first_name", read_only=True
    )
    products = ProductSerializer(
        many=True,
        source="ordered_products",
        read_only=True,
    )

    class Meta:
        model = Order
        fields = ["id", "status", "created_at", "buyer", "products",]
        read_only_fields = ["id", "created_at", "buyer", "products",]
