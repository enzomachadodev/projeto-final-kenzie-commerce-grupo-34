from django.db import models


class Cart(models.Model):
    buyer = models.ForeignKey(
        "users.User",
        related_name="user_cart",
        on_delete=models.CASCADE,
    )


# Create your models here.
