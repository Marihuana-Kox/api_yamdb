from rest_framework import permissions


class CustomPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.method in permissions.SAFE_METHODS or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(
            obj.author == request.user
            or request.user.role == "admin"
            or request.user.role == "moderator"
        )
