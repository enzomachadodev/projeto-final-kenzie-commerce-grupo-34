from django.db import models
import ipdb


class Product(models.Model):
    name = models.CharField(max_length=20)
    image_url = models.TextField(null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField()
    category = models.CharField(max_length=20)
    stock = models.IntegerField()

    cart = models.ManyToManyField(
        "carts.Cart",
        through="products.CartProducts",
        related_name="products",
    )

    seller = models.ForeignKey(
        "users.User",
        related_name="user_products",
        on_delete=models.CASCADE,
    )

    order = models.ManyToManyField(
        "orders.Order",
        through="products.OrderProducts",
        related_name="ordered_products",
    )


class CartProducts(models.Model):
    product = models.ForeignKey(
        "products.Product",
        on_delete=models.CASCADE,
        related_name="products_cart_pivo",
    )

    cart = models.ForeignKey(
        "carts.Cart",
        on_delete=models.CASCADE,
        related_name="cart_products_pivo",
    )

    quantity = models.IntegerField(default=1)

    @property
    def cauculate_total(self):
        return self.product.price * self.quantity


class OrderProducts(models.Model):
    product = models.ForeignKey(
        "products.Product",
        on_delete=models.CASCADE,
        related_name="products_order_pivo",
    )

    order = models.ForeignKey(
        "orders.Order",
        on_delete=models.CASCADE,
        related_name="order_products_pivo",
    )

    quantity = models.IntegerField()

    @property
    def calculate_total(self):
        return self.product.price * self.quantity
