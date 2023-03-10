from django.db import models


class Address(models.Model):
    street = models.CharField(max_length=40)
    zip_code = models.CharField(max_length=10)
    number = models.IntegerField()
    complement = models.TextField(null=True)
    city = models.CharField(max_length=20)
    state = models.CharField(max_length=20)

    user = models.OneToOneField(
        "users.User",
        related_name="address",
        on_delete=models.CASCADE,
    )


# Create your models here.
