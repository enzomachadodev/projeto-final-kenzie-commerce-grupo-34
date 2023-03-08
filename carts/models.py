from django.db import models


class Cart(models.Model):
    buyer = models.OneToOneField(
        "users.User",
        related_name="cart",
        on_delete=models.CASCADE,
    )
