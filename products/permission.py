
from rest_framework import permissions
from rest_framework.views import View

SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')


class IsSellerOrAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view: View) -> bool:

        return bool(
            request.method in SAFE_METHODS or request.user.is_superuser or request.user.is_authenticated and request.user.is_seller
        )
