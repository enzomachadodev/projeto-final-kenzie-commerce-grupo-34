from rest_framework import permissions
from rest_framework.views import View

from users.models import User


class IsSeller(permissions.BasePermission):
    def has_permission(self, request, view: View) -> bool:
        return request.user.is_authenticated and request.user.is_seller


class IsProductOwner(permissions.BasePermission):
    def has_object_permission(self, request, view: View, obj: User):
        return (
            request.user.is_authenticated
            and request.user.is_seller
            and obj.seller == request.user
        )
