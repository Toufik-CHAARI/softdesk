from rest_framework import permissions

class IsSuperuserOrSelf(permissions.BasePermission):
    """
    Custom permission to only allow superusers to edit/delete any user and normal users to edit/delete themselves.
    """

    def has_object_permission(self, request, view, obj):
        # Check if user is superuser
        if request.user.is_superuser:
            return True
        # Check if the user is trying to access or modify their own account
        return obj == request.user
