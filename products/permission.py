from rest_framework import permissions
from rest_framework.views import View


class IsSeller(permissions.BasePermission):
    def has_permission(self, request, view: View) -> bool:
        return request.user.is_authenticated and request.user.is_seller
