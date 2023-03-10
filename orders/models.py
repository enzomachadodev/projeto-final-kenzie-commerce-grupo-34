from django.db import models


class StatusOptions(models.TextChoices):
    REALIZADO = "PEDIDO REALIZADO"
    ANDAMENTO = "EM ANDAMENTO"
    ENTREGUE = "ENTREGUE"


class Order(models.Model):
    status = models.CharField(
        choices=StatusOptions.choices, default=StatusOptions.REALIZADO, max_length=40
    )

    created_at = models.DateTimeField(auto_now_add=True)

    buyer = models.ForeignKey(
        "users.User",
        related_name="user_orders",
        on_delete=models.CASCADE,
    )
    seller = models.ForeignKey(
        "users.User",
        related_name="seller_orders",
        on_delete=models.CASCADE,
    )

    @property
    def calculate_total(self):
        total = 0
        for obj in self.order_products_pivo.all():
            value = obj.quantity * obj.product.price
            total += value
        return total
