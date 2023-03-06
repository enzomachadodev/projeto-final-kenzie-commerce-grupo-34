from django.db import models


class Status(models.TextChoices):
    realizado = "PEDIDO REALIZADO"
    andamento = "EM ANDAMENTO"
    entregue = "ENTREGUE"


class Order(models.Model):
    status = models.CharField(
        choices=Status.choices, default=Status.realizado, max_length=40
    )
    created_at = models.DateField(auto_now_add=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField()
    category = models.CharField(max_length=20)

    buyer = models.ForeignKey(
        "users.User",
        related_name="user_orders",
        on_delete=models.CASCADE,
    )


# Create your models here.
