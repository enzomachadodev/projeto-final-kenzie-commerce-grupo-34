from rest_framework import permissions
from rest_framework.views import View


class IsCartNotEmptyOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view: View) -> bool:
        return (
            request.method in permissions.SAFE_METHODS
            or len(request.user.cart.products.all()) > 0
        )

class IsSellerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view: View) -> bool:
        return request.method in permissions.SAFE_METHODS or request.user.is_seller