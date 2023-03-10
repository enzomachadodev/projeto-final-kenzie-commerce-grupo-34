from rest_framework.test import APITestCase
from users.models import User
from adresses.models import Address
from rest_framework import status
from carts.models import Cart


class TestUserRegistration(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.BASE_URL = "/api/users/"

    def test_create_user(self):
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
        response = self.client.post(
            self.BASE_URL,
            data=user_data,
            format='json'
        )

        added_user = User.objects.last()
        added_address = Address.objects.last()
        added_cart = Cart.objects.last()

        expected_data = {
            "id": added_user.pk,
            "username": "gabriel",
            "email": "gabriel@kenzie.com",
            "first_name": "gabriel",
            "last_name": "sobrenome",
            "photo_url": None,
            "is_superuser": True,
            "is_seller": True,
            "address": {
              "id": added_address.pk,
              "street": "rua teste",
              "zip_code": "123456789",
              "number": 47,
              "complement": None,
              "city": "maceió",
              "state": "alagoas"
            },
            "cart": {
              "id": added_cart.pk,
              "cart_products_pivo": [],
              "cart_total": 0
            }
        }
        
        returned_data = response.json()

        msg = (
            "Verifique se as informações do usuário retornada no POST "
            + f"em {self.BASE_URL} estão corretas."
        )
        self.assertDictEqual(expected_data, returned_data, msg)

        expected_status_code = status.HTTP_201_CREATED
        msg = (
            "Verifique se o status code retornado no POST "
            + f"em {self.BASE_URL} é {expected_status_code}"
        )
        self.assertEqual(response.status_code, expected_status_code, msg)

        msg = "Verifique se o password foi hasheado corretamente"
        self.assertTrue(added_user.check_password(user_data["password"]), msg)

    def test_user_register_without_required_fields(self):
        response = self.client.post(self.BASE_URL, data={}, format='json')

        resulted_data: dict = response.json()

        expected_fields = {
          "username",
          "password",
          "email",
          "first_name",
          "last_name",
          "address"
        }

        returned_fields = set(resulted_data.keys())

        msg = (
            "Verifique se todas as chaves obrigatórias são retornadas"
            + f"ao tentar criar um usuário sem dados"
        )
        self.assertSetEqual(expected_fields, returned_fields, msg)

        expected_status_code = status.HTTP_400_BAD_REQUEST
        msg = (
            "Verifique se o status code retornado no POST "
            + f"em {self.BASE_URL} é {expected_status_code}"
        )
        self.assertEqual(response.status_code, expected_status_code, msg)

    def test_create_non_unique_username_or_email_user(self):
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

        self.client.post(self.BASE_URL, data=user_data, format='json')
        response = self.client.post(self.BASE_URL, data=user_data, format='json')

        expected_fields = {
            "username",
            "email"
        }
        
        returned_data = response.json()
        returned_fields = set(returned_data.keys())

        msg = (
            "Verifique se as informações do usuário retornada no POST "
            + f"em `{self.BASE_URL}` estão corretas."
        )
        self.assertSetEqual(expected_fields, returned_fields, msg)

        resulted_username_message = returned_data["username"][0]
        resulted_email_message = returned_data["email"][0]

        expected_username_message = "A user with that username already exists."
        expected_email_message = "This field must be unique."

        msg = (
            "Verifique a mensagem de erro quando criando usuário com username repetido"
        )
        self.assertEqual(expected_username_message, resulted_username_message, msg)

        msg = "Verifique a mensagem de erro quando criando usuário com email repetido"
        self.assertEqual(expected_email_message, resulted_email_message, msg)

        expected_status_code = status.HTTP_400_BAD_REQUEST

        msg = (
            "Verifique se o status code retornado do POST "
            + f"em `{self.BASE_URL}` é {expected_status_code}"
        )
        self.assertEqual(expected_status_code, response.status_code, msg)
