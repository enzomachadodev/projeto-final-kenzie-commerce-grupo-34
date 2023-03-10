from products.models import Product
from django.contrib.auth.models import AbstractUser
from django.db.models import QuerySet


def create_product_with_user(
        user: AbstractUser, product_data: dict = None
  ) -> Product:
    if not product_data:
        product_data = {
          "name": "Produto",
          "price": 200.00,
          "description": "Isso é um produto teste",
          "category": "Testes",
          "stock": 100
        }

        product = Product.objects.create(**product_data, user=user)

        return product


def create_multiple_products_with_user(
        user: AbstractUser, products_count: int
) -> QuerySet[Product]:
    products_data = [
        {
          "name": f"Produto {index}",
          "price": 200.00,
          "description": f"Teste de número {index}",
          "category": "Testes",
          "stock": 100,
          "user": user
        }
        for index in range(1, products_count + 1)
    ]
    products_objects = [
        Product(**product_data) for product_data in products_data
    ]
    products = Product.objects.bulk_create(products_objects)

    return products
