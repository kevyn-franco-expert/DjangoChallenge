from rest_framework import permissions


class IsSuperuser(permissions.BasePermission):
    """
    return superuser validation
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_superuser
