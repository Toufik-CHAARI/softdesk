from rest_framework import permissions
from .models import Contributor,Project,Issue

class IsProjectContributorOrAuthor(permissions.BasePermission):
    """
    Custom permission to only allow contributors or the author of a project to view its content.
    """

    def has_object_permission(self, request, view, obj):
        # Check if the user is the author of the project
        if isinstance(obj, Project):
            if obj.author == request.user:
                return True
            return Contributor.objects.filter(user=request.user, project=obj).exists()
        
        # If it's an issue or a comment, check the related project's contributors and author.
        project_related = obj.project if isinstance(obj, Issue) else obj.issue.project
        if project_related.author == request.user:
            return True
        return Contributor.objects.filter(user=request.user, project=project_related).exists()



class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit or delete it.
    """
    
    def has_object_permission(self, request, view, obj):
        # Permissions are only allowed to the owner of the comment.
        # Adjust the 'author' field accordingly if your model uses a different field name.
        return obj.author == request.user