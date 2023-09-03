from rest_framework import permissions


class IsAdminOrSuperUser(permissions.BasePermission):
    """Permision allowing all methods only for admin and superuser roles."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_superuser or request.user.is_admin
        )


class IsAdminModeratorSuperUserAuthorOrReadOnly(permissions.BasePermission):
    """Permision allowing {SAFE_METHODS} to all users and
        other methods only for authenticated users
        that are either author of the object, moderators, admins or superusers.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (
            request.user.is_superuser
            or request.user.is_admin
            or request.user.is_moderator
            or (request.user == obj.author)
        )


class IsAdminOrReadOnly(permissions.BasePermission):
    """Permision allowing {SAFE_METHODS} to all users and
        other methods only for admin and superuser roles.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and (
            request.user.is_superuser or request.user.is_admin
        )
