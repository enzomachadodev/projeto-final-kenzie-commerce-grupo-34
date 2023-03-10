import smtplib
from email.message import EmailMessage

import os
import dotenv


from rest_framework import serializers

from .models import Order, StatusOptions

from products.serializers import ProductSerializer
from products.models import OrderProducts, Product

from users.models import User

import smtplib
from email.message import EmailMessage
import ipdb

dotenv.load_dotenv()


def choices_error_message(choices_class):
    valid_choices = [choice[0] for choice in choices_class.choices]
    message = ", ".join(valid_choices).rsplit(",", 1)

    return "Choose between " + " and".join(message) + "."


def send_seller_email(order, message):
    body_message = f"""
    {message}
    \n
    Id do pedido: {order.id}
    \n
    Loja: {order.seller.username}
    \n
    Data: {order.created_at}
    \n
    Status: {order.status}
    \n
    """

    email_address = os.getenv("DB_EMAIL")
    email_password = os.getenv("DB_EMAIL_PASSWORD_PYTHON")
    msg = EmailMessage()
    msg["Subject"] = "PEDIDO REALIZADO"
    msg["From"] = email_address
    msg["To"] = order.buyer.email
    msg.set_content(body_message)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(email_address, email_password)
        smtp.send_message(msg)

class ProductOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "image_url",
            "price",
            "description",
            "category",
            "seller",
        ]


class OrderProductsSerializer(serializers.ModelSerializer):
    product = ProductOrderSerializer(read_only=True)
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
        sellers = []
        orders = []
        for cart_product_obj in cart.cart_products_pivo.all():
            seller = cart_product_obj.product.seller
            if seller not in sellers:
                sellers.append(seller)

        for seller in sellers:
            order = Order.objects.create(seller=seller, **validated_data)

            for cart_product_obj in cart.cart_products_pivo.all():
                if cart_product_obj.product.seller == seller:
                    OrderProducts.objects.create(
                        order=order,
                        product=cart_product_obj.product,
                        quantity=cart_product_obj.quantity,
                    )
            orders.append(order)
            email_message =  'Parabéns! Sua compra foi realizada com sucesso e chegará em breve.'
            send_seller_email(order=order, message= email_message)

        cart.clear()
        cart.save()
        return orders

    def update(self, instance: Order, validated_data: dict) -> Order:
        if validated_data.get("status"):
            instance.status = validated_data["status"]
            instance.save()
            email_message = 'O Status do seu pedido foi atualizado'
            send_seller_email(order=instance, message=email_message)
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
            "seller",
            "ordered_products",
            "order_total",
        ]
        extra_kwargs = {
            "status": {
                "error_messages": {
                    "invalid_choice": choices_error_message(StatusOptions),
                }
            },
            "seller": {"read_only": True},
        }
