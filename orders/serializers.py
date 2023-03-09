import smtplib
from email.message import EmailMessage

import os
import dotenv


from rest_framework import serializers

from .models import Order, StatusOptions

from products.serializers import ProductSerializer
from products.models import OrderProducts


import smtplib
from email.message import EmailMessage

dotenv.load_dotenv()


def choices_error_message(choices_class):
    valid_choices = [choice[0] for choice in choices_class.choices]
    message = ", ".join(valid_choices).rsplit(",", 1)

    return "Choose between " + " and".join(message) + "."


def send_seller_email(seller_email, product_name, buyer):
    body_message = f"""{buyer.first_name} {buyer.last_name} comprou {product_name}"""

    email_address = os.getenv("DB_EMAIL")
    email_password = os.getenv("DB_EMAIL_PASSWORD_PYTHON")

    msg = EmailMessage()
    msg["Subject"] = "Alguém comprou uma de suas mercadorias"
    msg["From"] = email_address
    msg["To"] = seller_email
    msg.set_content(body_message)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(email_address, email_password)
        smtp.send_message(msg)


class OrderProductsSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    total_price = serializers.ReadOnlyField(source="calculate_total")

    class Meta:
        model = OrderProducts
        fields = [
            "product",
            "quantity",
            "total_price",
        ]
        read_only_fields = ["quantity"]


class OrderSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        cart = validated_data.pop("cart")

        order = Order.objects.create(**validated_data)

        for cart_product_obj in cart.cart_products_pivo.all():
            send_seller_email(
                cart_product_obj.product.seller.email,
                cart_product_obj.product.name,
                order.buyer,
            )
            OrderProducts.objects.create(
                order=order,
                product=cart_product_obj.product,
                quantity=cart_product_obj.quantity,
            )

        cart.products.clear()
        order.save()
        return order

    def update(self, instance: Order, validated_data: dict) -> Order:
        if validated_data.get("status"):
            instance.status = validated_data["status"]
            instance.save()
        return instance

    buyer = serializers.CharField(
        max_length=40, source="buyer.first_name", read_only=True
    )

    ordered_products = OrderProductsSerializer(
        many=True,
        read_only=True,
        source="order_products_pivo",
    )

    order_total = serializers.ReadOnlyField(source="calculate_total")

    class Meta:
        model = Order
        fields = [
            "id",
            "status",
            "created_at",
            "buyer",
            "ordered_products",
            "order_total",
        ]
        extra_kwargs = {
            "status": {
                "error_messages": {
                    "invalid_choice": choices_error_message(StatusOptions),
                }
            },
        }
