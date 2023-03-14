from rest_framework.test import APITestCase
from rest_framework.views import status
from tests.factories.user_factories import create_user_with_token
from tests.factories.product_factories import (
    create_product_with_user,
    create_multiple_products_with_user,
)


# class TestCartView(APITestCase):
#     @classmethod
#     def setUpTestData(cls) -> None:
#         cls.BASE_URL = "/api/cart"

#     def test_add_product_to_cart(self):
#         user, token = create_user_with_token()
#         self.client.credentials(HTTP_AUTHORIZATION="Bearer " + str(token.access_token))

#         product_data = {
#             "name": "Cake",
#             "price": 25,
#             "description": "The cake is a lie",
#             "category": "Bakery",
#             "stock": 4,
#         }

#         product = self.client.post("/api/products/", data=product_data, format="json")

#         expected_data = {
#             "id": 1,
#             "cart_products_pivo": [
#                 {
#                     "product": {
#                         "id": product.data["id"],
#                         "name": "Cake",
#                         "image_url": None,
#                         "price": 25.00,
#                         "description": "The cake is a lie",
#                         "category": "Bakery",
#                         "is_avaliable": True,
#                         "stock": 4,
#                         "seller": user.pk,
#                     },
#                     "quantity": 1,
#                     "total_price": 25.00,
#                 }
#             ],
#             "cart_total": 25.00,
#         }

#         response = self.client.post(
#             f'{self.BASE_URL}/{product.data["id"]}/', format="json"
#         )

#         expected_status_code = status.HTTP_200_OK
#         msg = (
#             "Verifique se o status code retornado do POST "
#             + f"em `{self.BASE_URL}` é {expected_status_code}"
#         )
#         self.assertEqual(expected_status_code, response.status_code, msg)

#         response_data: dict = response.json()

#         returned_fields = set(response_data.keys())
#         msg = (
#             "Verifique se todas as chaves obrigatórias "
#             + f"são retornadas ao tentar criar um produto sem dados"
#         )

#         self.assertEqual(expected_data, response_data, msg)
