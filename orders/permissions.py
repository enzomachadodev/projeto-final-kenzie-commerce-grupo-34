from rest_framework import permissions
from rest_framework.views import View


class IsCartNotEmptyOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view: View) -> bool:
        self.message = "Your cart is empty"

        return (
            request.method in permissions.SAFE_METHODS
            or len(request.user.cart.products.all()) > 0
        )


class IsSellerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view: View) -> bool:
        self.message = "You are not a seller or administrator"

        return request.method in permissions.SAFE_METHODS or request.user.is_seller


class IsProductAvailableOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view: View) -> bool:
        self.message = "Product not in stock"

        if request.method == "GET":
            return True

        for product in request.user.cart.products.all():
            if product.stock == 0:
                return False
            if (
                request.user.cart.cart_products_pivo.filter(product=product)
                .first()
                .quantity
                > product.stock
            ):
                self.message = "Product not enough in stock"

                return False

        return True
