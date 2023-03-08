from django.db import models
import ipdb


class Cart(models.Model):
    buyer = models.OneToOneField(
        "users.User",
        related_name="cart",
        on_delete=models.CASCADE,
    )

    @property
    def cauculate_total(self):
        total = 0
        for obj in self.cart_products_pivo.all():
            value = obj.quantity * obj.product.price
            total += value
        return total
