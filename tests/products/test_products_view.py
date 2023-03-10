from rest_framework.test import APITestCase
from rest_framework.views import status
from tests.factories.user_factories import create_user_with_token
from tests.factories.product_factories import create_product_with_user, create_multiple_products_with_user


class TestProductsView(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.BASE_URL = '/api/products/'

    """ def test_products_listing_pagination(self):
        user, token = create_user_with_token()
        product_count = 4
        create_multiple_products_with_user(user, product_count)

        response = self.client.get(self.BASE_URL)
        response_data = response.json()
        response_pagination_keys = set(response_data.keys())
        expected_pagination_keys = {"count", "next", "previous", "results"}
        msg = "Verifique se a paginação está sendo feita corretamente"

        self.assertEqual(expected_pagination_keys, response_pagination_keys, msg)

        response_len = len(response_data['results'])
        expected_len = 2
        msg = "Verifique se a paginação está retornando apenas dois items de cada vez"
        self.assertEqual(expected_len, response_len, msg) """

    def test_create_product_without_required_fields(self):
        user, token = create_user_with_token()
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + str(token.access_token))
        response = self.client.post(self.BASE_URL, data={}, format='json')

        expected_status_code = status.HTTP_400_BAD_REQUEST
        msg = (
                "Verifique se o status code retornado do POST sem todos os "
                + f"campos obrigatórios em `{self.BASE_URL}` é {expected_status_code}"
            )
        self.assertEqual(expected_status_code, response.status_code, msg)

        response_data: dict = response.json()
        expected_fields = {
            "name",
            "price",
            "description",
            "category",
            "stock"
        }
        returned_fields = set(response_data.keys())
        msg = (
                "Verifique se todas as chaves obrigatórias "
                + f"são retornadas ao tentar criar um produto sem dados"
            )

        self.assertEqual(expected_fields, returned_fields, msg)

    def test_create_product_without_token(self):
        response = self.client.post(self.BASE_URL, data={}, format='json')
        expected_status_code = status.HTTP_401_UNAUTHORIZED
        msg = (
                "Verifique se o status code retornado do POST "
                + f"em `{self.BASE_URL}` é {expected_status_code}"
        )
        self.assertEqual(expected_status_code, response.status_code, msg)

        expected_data = {"detail": "Authentication credentials were not provided."}
        response_data = response.json()
        msg = (
            "Verifique se a mensagem de retorno do POST sem token"
            + f"em `{self.BASE_URL}` está correta."
        )
        self.assertDictEqual(expected_data, response_data, msg)

    def test_create_product(self):
        product_data = {
          "name": "produto1",
          "price": 200.00,
          "description": "Um produto",
          "category": "Categoria Teste",
          "stock": 100
        }
        user, token = create_user_with_token()
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + str(token.access_token)
        )
        response = self.client.post(self.BASE_URL, data=product_data, format='json')
        expected_status_code = status.HTTP_201_CREATED
        msg = (
                "Verifique se o status code retornado do POST "
                + f"em `{self.BASE_URL}` é {expected_status_code}"
        )
        self.assertEqual(expected_status_code, response.status_code, msg)

        expected_data = {
            "id": 1,
            "name": "produto1",
            "image_url": None,
            "price": "200.00",
            "description": "Um produto",
            "category": "Categoria Teste",
            "stock": 100,
            "seller": user.pk
        }
        response_data = response.json()
        msg = (
            "Verifique se as informações retornadas no POST "
            + f"em `{self.BASE_URL}` estão corretas."
        )
        self.assertDictEqual(expected_data, response_data, msg)

    def test_create_products_without_been_seller(self):
        user_data = {
            "username": "gabriel",
            "password": "1234",
            "email": "gabriel@kenzie.com",
            "first_name": "gabriel",
            "last_name": "sobrenome",
            "is_seller": False,
            "is_superuser": False,
            "address": {
              "street": "rua teste",
              "zip_code": "123456789",
              "number": 47,
              "city": "maceió",
              "state": "alagoas"
            }
        }
        user, token = create_user_with_token(user_data)
        product_data = {
          "name": "produto1",
          "price": 200.00,
          "description": "Um produto",
          "category": "Categoria Teste",
          "stock": 100
        }
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + str(token.access_token)
        )
        response = self.client.post(self.BASE_URL, data=product_data, format='json')
        expected_status_code = status.HTTP_403_FORBIDDEN
        msg = (
                "Verifique se o status code retornado do POST "
                + f"em `{self.BASE_URL}` é {expected_status_code}"
        )
        self.assertEqual(expected_status_code, response.status_code, msg)

    def test_update_products_without_token(self):
        response = self.client.patch(self.BASE_URL, format='json')
        expected_status_code = status.HTTP_401_UNAUTHORIZED
        msg = (
            "Verifique se o status code retornado do PATCH sem token "
            + f"em `{self.BASE_URL}` é {expected_status_code}"
        )
        self.assertEqual(expected_status_code, response.status_code, msg)

        expected_data = {"detail": "Authentication credentials were not provided."}
        response_data = response.json()
        msg = (
            "Verifique se os dados retornados do PATCH sem token "
            + f"em `{self.BASE_URL}` é {expected_data}"
        )
        self.assertDictEqual(expected_data, response_data, msg)

    def test_update_products_without_been_owner(self):
        owner, token1 = create_user_with_token()
        self.client.credentials(
                HTTP_AUTHORIZATION="Bearer " + str(token1.access_token)
        )
        product_data = {
          "name": "produto1",
          "price": 200.00,
          "description": "Um produto",
          "category": "Categoria Teste",
          "stock": 100
        }
        product = self.client.post(self.BASE_URL, data=product_data, format='json')

        user_data = {
            "username": "josiel",
            "password": "1234",
            "email": "josiel@kenzie.com",
            "first_name": "josi",
            "last_name": "el",
            "is_seller": True,
            "is_superuser": False,
            "address": {
              "street": "rua teste",
              "zip_code": "123456789",
              "number": 47,
              "city": "testando",
              "state": "mg"
            }
        }
        user, token2 = create_user_with_token(user_data)
        self.client.credentials(
                HTTP_AUTHORIZATION="Bearer " + str(token2.access_token)
        )
        patch_data = {
          "name": "produto_PATCHED",
          "price": 20.00
        }

        response = self.client.patch(f"{self.BASE_URL}{product.data['id']}/", data=patch_data, format='json')
        expected_status_code = status.HTTP_401_UNAUTHORIZED
        msg = (
            "Verifique se o status code retornado do PATCH com token correto "
            + f"em `{self.BASE_URL}{product.data['id']}` é {expected_status_code}"
        )
        self.assertEqual(expected_status_code, response.status_code, msg)
        expected_data = {"detail": "Authentication credentials were not provided."}
        response_data = response.json()
        msg = (
            "Verifique se os dados retornados do PATCH com token correto em "
            + f"em `{self.BASE_URL}` é {expected_data}"
        )
        self.assertDictEqual(expected_data, response_data, msg)

    def test_update_product(self):
        user, token = create_user_with_token()
        self.client.credentials(
                HTTP_AUTHORIZATION="Bearer " + str(token.access_token)
        )
        product_data = {
          "name": "produto1",
          "price": 200.00,
          "description": "Um produto",
          "category": "Categoria Teste",
          "stock": 100
        }       
        product = self.client.post(self.BASE_URL, data=product_data, format='json')
        patch_data = {
          "name": "ALTEREI O PRODUTO",
          "price": 6.99,
          "description": "outra coisa",
          "category": "FUNCIONA",
          "stock": 50	
        }
        response = self.client.patch(f"{self.BASE_URL}{product.data['id']}/", data=patch_data, format='json')
        expected_status_code = status.HTTP_200_OK
        msg = (
            "Verifique se o status code retornado do PATCH sem token correto "
            + f"em `{self.BASE_URL}` é {expected_status_code}"
        )
        self.assertEqual(expected_status_code, response.status_code, msg)

        expected_data = {
          "id": product.data['id'],
          "name": response.data["name"],
          "image_url": None,
          "price": response.data["price"],
          "description": response.data["description"],
          "category": response.data["category"],
          "stock": response.data["stock"],
          "seller": user.pk
        }
        response_data = response.json()
        msg = (
            "Verifique se o data retornado do PATCH com token correto "
            + f"em `{self.BASE_URL}` é {expected_data}"
        )
        self.assertEqual(expected_data, response_data, msg)
