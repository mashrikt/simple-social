from rest_framework import permissions


class IsCreatorOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if not(request.user and request.user.is_authenticated):
            return False

        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the creator of the obj.
        return obj.created_by == request.user
