from django.contrib.auth.models import AbstractUser
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import User
from carts.models import Cart
from adresses.models import Address


def create_user_with_token(user_data=None) -> tuple[AbstractUser, RefreshToken]:
    if not user_data:
        user_data = {
          "username": "gabriel",
          "password": "1234",
          "email": "gabriel@kenzie.com",
          "first_name": "gabriel",
          "last_name": "sobrenome",
          "is_seller": True,
          "is_superuser": True,
          "address": {
            "street": "rua teste",
            "zip_code": "123456789",
            "number": 47,
            "city": "maceió",
            "state": "alagoas"
          }
        }

    address = user_data.pop("address")
    user = User.objects.create_user(**user_data)
    Address.objects.create(**address, user=user)
    Cart.objects.create(buyer=user)

    user_token = RefreshToken.for_user(user)

    return user, user_token
