from rest_framework import permissions
from .models import Contributor, Project, Issue


class IsProjectContributorOrAuthorOrSuperuser(permissions.BasePermission):
    """
    Custom permission to check if the user is a contributor to a project,
    the project's author, or a superuser.This permission is useful
    in scenarios where access needs to be limited to:
    - Superusers (full access rights)
    - The author of the project (owner rights)
    - Contributors to the project (limited rights)
    Additional checks are also performed for issues
    associated with a project.
    """

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True

        if isinstance(obj, Issue):
            if obj.author == request.user:
                return True

            project_related = obj.project
            is_contributor = Contributor.objects.filter(
                user=request.user, project=project_related
            ).exists()
            if request.method in permissions.SAFE_METHODS and is_contributor:
                return True

            return False

        if isinstance(obj, Project):
            if obj.author == request.user:
                return True
            return Contributor.objects.filter(
                user=request.user, project=obj
            ).exists()

        if isinstance(obj, Contributor):
            related_project = obj.project
            if related_project.author == request.user:
                return True

            return Contributor.objects.filter(
                user=request.user, project=related_project
            ).exists()

        """
        For other objects (like Comments), check the
        related project's contributors and author
        """
        project_related = (
            obj.project if hasattr(obj, "project") else obj.issue.project
        )
        if project_related.author == request.user:
            return True
        return Contributor.objects.filter(
            user=request.user, project=project_related
        ).exists()


class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit or delete it.
    """

    def has_object_permission(self, request, view, obj):
        # Permissions are only allowed to the owner of the comment.
        return obj.author == request.user
