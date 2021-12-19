from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import BasePermission

from accounts.models import CustomUser
from accounts.utils import get_user


class TokenPermission(BasePermission):

    def has_permission(self, request, view):
        token = request.COOKIES.get('auth_token')
        if token:
            try:
                user = CustomUser.objects.get(auth_token=token)
            except ObjectDoesNotExist:
                return False
            else:
                return bool(token and user.is_active)
        else:
            return False


class ManufacturerPermission(BasePermission):
    def has_permission(self, request, view):
        user = get_user(request)
        return bool(user.is_manufacturer)

