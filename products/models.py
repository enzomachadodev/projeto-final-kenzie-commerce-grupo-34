from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=20)
    image_url = models.TextField(null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField()
    category = models.CharField(max_length=20)
    stock = models.IntegerField()

    cart = models.ManyToManyField(
        "carts.Cart",
        related_name="cart_products",
    )

    seller = models.ForeignKey(
        "users.User",
        related_name="user_products",
        on_delete=models.CASCADE,
    )

    order = models.ManyToManyField(
        "orders.Order",
        related_name="ordered_products",
    )
