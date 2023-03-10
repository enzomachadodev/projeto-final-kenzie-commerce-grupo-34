from rest_framework.test import APITestCase
from rest_framework import status
from tests.factories.user_factories import create_user_with_token
from users.models import User


class TestUserDetailView(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:

        cls.user_1, token_1 = create_user_with_token()
        cls.access_token_1 = str(token_1.access_token)

        user_data2 = {
          "username": "felipe",
          "password": "1234",
          "email": "felps@kenzie.com",
          "first_name": "Felipe",
          "last_name": "Siqueira",
          "is_seller": True,
          "is_superuser": True,
          "address": {
            "street": "rua dois",
            "zip_code": "987654321",
            "number": 98,
            "city": "Itabirito",
            "state": "Minas Gerais"
          }       
        }

        cls.user_2, token_2 = create_user_with_token(user_data=user_data2)
        cls.access_token_2 = str(token_2.access_token)
        cls.BASE_URL = f"/api/users/{cls.user_1.id}/"

    def test_get_user_without_token(self):
        response = self.client.get(self.BASE_URL, format='json')

        expected_status_code = status.HTTP_401_UNAUTHORIZED
        msg = (
            "Verifique se o status code retornado do GET sem token "
            + f"em `{self.BASE_URL}` é {expected_status_code}"
        )
        self.assertEqual(expected_status_code, response.status_code, msg)
        expected_data = {
            "detail": "Authentication credentials were not provided."
        }
        
        response_data = response.json()
        msg = (
            "Verifique se os dados retornados do GET sem token "
            + f"em `{self.BASE_URL}` é {expected_data}"
        )
        self.assertDictEqual(expected_data, response_data, msg)

    def test_get_user_with_another_user_token(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.access_token_2
        )
        response = self.client.get(self.BASE_URL, format="json")
        expected_status_code = status.HTTP_200_OK
        msg = (
            "Verifique se o status code retornado do GET sem token correto "
            + f"em `{self.BASE_URL}` é {expected_status_code}"
        )
        self.assertEqual(expected_status_code, response.status_code, msg)
        expected_message = {
            "id": self.user_1.pk,
            "username": self.user_1.username,
            "email": self.user_1.email,
            "first_name": self.user_1.first_name,
            "last_name": self.user_1.last_name,
            "photo_url": self.user_1.photo_url,
            "is_superuser": self.user_1.is_superuser,
            "is_seller": self.user_1.is_seller,
            "address": {
                "id": self.user_1.address.pk,
                "street": self.user_1.address.street,
                "zip_code": self.user_1.address.zip_code,
                "number": self.user_1.address.number,
                "complement": self.user_1.address.complement,
                "city": self.user_1.address.city,
                "state": self.user_1.address.state
            },
            "cart": {
                "id": self.user_1.cart.pk,
                "cart_products_pivo": [],
                "cart_total": 0
            }
        }

        resulted_message = response.json()
        msg = (
            f"Verifique se a mensagem retornada do GET em {self.BASE_URL} está correta"
        )
        self.assertDictEqual(expected_message, resulted_message, msg)

    def test_get_user_with_corrent_user_token(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.access_token_1
        )
        response = self.client.get(self.BASE_URL, format="json")
        expected_status_code = status.HTTP_200_OK
        msg = (
            "Verifique se o status code retornado do GET com token correto "
            + f"em `{self.BASE_URL}` é {expected_status_code}"
        )
        self.assertEqual(expected_status_code, response.status_code, msg)

        expected_data = {
            "id": self.user_1.pk,
            "username": self.user_1.username,
            "email": self.user_1.email,
            "first_name": self.user_1.first_name,
            "last_name": self.user_1.last_name,
            "photo_url": self.user_1.photo_url,
            "is_superuser": self.user_1.is_superuser,
            "is_seller": self.user_1.is_seller,
            "address": {
              "id": self.user_1.address.pk,
              "street": self.user_1.address.street,
              "zip_code": self.user_1.address.zip_code,
              "number": self.user_1.address.number,
              "complement": self.user_1.address.complement,
              "city": self.user_1.address.city,
              "state": self.user_1.address.state
            },
            "cart": {
              "id": self.user_1.cart.pk,
              "cart_products_pivo": [],
              "cart_total": 0
            }
        }
        response_data = response.json()
        msg = (
            "Verifique se os dados retornados do GET com token correto em "
            + f"em `{self.BASE_URL}` é {expected_data}"
        )
        self.assertDictEqual(expected_data, response_data, msg)
        
    def test_update_user_without_token(self):
        response = self.client.patch(self.BASE_URL, format='json')
        expected_status_code = status.HTTP_401_UNAUTHORIZED

        msg = (
            "Verifique se o status code retornado do GET sem token "
            + f"em `{self.BASE_URL}` é {expected_status_code}"
        )
        self.assertEqual(expected_status_code, response.status_code, msg)

        expected_data = {
            "detail": "Authentication credentials were not provided."
        }

        resulted_data = response.json()

        msg = (
            "Verifique se os dados retornados do PATCH sem token "
            + f"em `{self.BASE_URL}` é {expected_data}"
        )
        self.assertDictEqual(expected_data, resulted_data, msg)

    def test_update_user_with_another_user_token(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.access_token_2
        )
        response = self.client.patch(self.BASE_URL, format='json')

        expected_status_code = status.HTTP_403_FORBIDDEN

        msg = (
            "Verifique se o status code retornado no PATCH com token de outra conta "
            + f"em `{self.BASE_URL}` é {expected_status_code}"
        )
        self.assertEqual(expected_status_code, response.status_code, msg)

        expected_message = {
            "detail": "You do not have permission to perform this action."
        }
        resulted_message = response.json()
        msg = f"Verifique se a mensagem retornada do PATCH em {self.BASE_URL} está correta"
        self.assertDictEqual(expected_message, resulted_message, msg)

    def test_update_user_with_correct_token(self):
        path_data = {
          "username": "Rodolfin",
          "first_name": "Rodolfo",
          "password": "5678"
        }
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.access_token_1
        )
        response = self.client.patch(self.BASE_URL, data=path_data, format='json')

        expected_status_code = status.HTTP_200_OK
        msg = (
            "Verifique se o status code retornado do PATCH com token correto "
            + f"em `{self.BASE_URL}` é {expected_status_code}"
        )
        self.assertEqual(expected_status_code, response.status_code, msg)

        expected_data = {
            "id": self.user_1.pk,
            "username": path_data["username"],
            "email": "gabriel@kenzie.com",
            "first_name": path_data["first_name"],
            "last_name": "sobrenome",
            "photo_url": None,
            "is_superuser": True,
            "is_seller": True,
            "address": {
              "id": self.user_1.address.pk,
              "street": "rua teste",
              "zip_code": "123456789",
              "number": 47,
              "complement": None,
              "city": "maceió",
              "state": "alagoas"
            },
            "cart": {
              "id": self.user_1.cart.pk,
              "cart_products_pivo": [],
              "cart_total": 0
            }
        }

        resulted_data = response.json()

        msg = (
            "Verifique se os dados retornados do PATCH com token correto em "
            + f"em `{self.BASE_URL}` é {expected_data}"
        )
        self.assertDictEqual(expected_data, resulted_data, msg)

        user = User.objects.first()
        msg = (
            f"Verifique se a senha está sendo atualizada no {response.request['REQUEST_METHOD']} em "
            + f"em `{self.BASE_URL}`"
        )
        self.assertTrue(user.check_password(path_data["password"]), msg)

    def test_delete_user_without_token(self):
        response = self.client.delete(self.BASE_URL, format='json')

        expected_status_code = status.HTTP_401_UNAUTHORIZED
        msg = (
            "Verifique se o status code retornado do DELETE sem token "
            + f"em `{self.BASE_URL}` é {expected_status_code}"
        )
        self.assertEqual(expected_status_code, response.status_code, msg)

        expected_data = {
            "detail": "Authentication credentials were not provided."
        }
        response_data = response.json()
        msg = (
            "Verifique se os dados retornados do DELETE sem token "
            + f"em `{self.BASE_URL}` é {expected_data}"
        )
        self.assertDictEqual(expected_data, response_data, msg)

    def test_delete_user_with_another_user_token(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.access_token_2
        )
        response = self.client.delete(self.BASE_URL, format="json")

        expected_status_code = status.HTTP_403_FORBIDDEN
        msg = (
            "Verifique se o status code retornado do DELETE sem token correto "
            + f"em `{self.BASE_URL}` é {expected_status_code}"
        )
        self.assertEqual(expected_status_code, response.status_code, msg)

        expected_data = {
            "detail": "You do not have permission to perform this action."
        }
        response_data = response.json()

        msg = f"Verifique se a mensagem retornada do DELETE em {self.BASE_URL} está correta"
        self.assertDictEqual(expected_data, response_data, msg)
  
    def test_delete_user_with_correct_user_token(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.access_token_1
        )
        response = self.client.delete(self.BASE_URL, format="json")

        expected_status_code = status.HTTP_204_NO_CONTENT
        msg = (
            "Verifique se o status code retornado do DELETE com token correto "
            + f"em `{self.BASE_URL}` é {expected_status_code}"
        )
        self.assertEqual(expected_status_code, response.status_code, msg)
