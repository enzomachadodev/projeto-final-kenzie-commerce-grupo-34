from rest_framework.test import APITestCase
from rest_framework import status


class TestUserLogin(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.BASE_URL = "/api/login/"

    def test_login(self):
        register_data = {
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
                "state": "alagoas",
            },
        }
        self.client.post("/api/users/", data=register_data, format="json")

        login_data = {"username": "gabriel", "password": "1234"}

        response = self.client.post(self.BASE_URL, data=login_data, format="json")

        expected_status_code = status.HTTP_200_OK

        msg = (
            "Verifique se o status code retornado no POST "
            + f"em {self.BASE_URL} é {expected_status_code}"
        )
        self.assertEqual(expected_status_code, response.status_code, msg)

        resulted_data: dict = response.json()

        expected_keys = {"refresh", "access"}

        returned_keys = set(resulted_data.keys())

        msg = (
            "Verifique se todas as chaves obrigatórias são retornadas "
            + f"ao tentar logar usuário"
        )
        self.assertSetEqual(expected_keys, returned_keys, msg)

    def test_login_with_wrong_credentials(self):
        register_data = {
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
                "state": "alagoas",
            },
        }
        self.client.post("/api/users/", data=register_data, format="json")

        login_data = {"username": "gabriel", "password": "5678"}

        response = self.client.post(self.BASE_URL, data=login_data, format="json")

        expected_status_code = status.HTTP_401_UNAUTHORIZED

        msg = (
            "Verifique se o status code retornado no POST "
            + f"em {self.BASE_URL} é {expected_status_code}"
        )
        self.assertEqual(expected_status_code, response.status_code, msg)

        resulted_data: dict = response.json()

        expected_keys = {"detail"}

        returned_keys = set(resulted_data.keys())

        msg = (
            "Verifique se todas as chaves obrigatórias são retornadas "
            + f"ao tentar logar usuário"
        )
        self.assertSetEqual(expected_keys, returned_keys, msg)

    def test_login_without_required_field(self):
        response = self.client.post(self.BASE_URL, data={}, format="json")

        expected_status_code = status.HTTP_400_BAD_REQUEST

        msg = (
            "Verifique se o status code retornado no POST "
            + f"em {self.BASE_URL} é {expected_status_code}"
        )
        self.assertEqual(expected_status_code, response.status_code, msg)

        resulted_data: dict = response.json()

        expected_keys = {"username", "password"}

        returned_keys = set(resulted_data.keys())

        msg = (
            "Verifique se todas as chaves obrigatórias são retornadas "
            + f"ao tentar logar usuário"
        )
        self.assertSetEqual(expected_keys, returned_keys, msg)
