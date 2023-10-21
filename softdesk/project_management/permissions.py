from rest_framework import permissions
from .models import Contributor,Project,Issue




class IsProjectContributorOrAuthorOrSuperuser(permissions.BasePermission):
    """
    Custom permission to only allow contributors, the author of a project, or superusers to view its content.
    This also provides additional checks for issues.
    """

    def has_object_permission(self, request, view, obj):
        # Check if the user is a superuser
        if request.user.is_superuser:
            return True
        
        # Logic specific to Issue
        if isinstance(obj, Issue):
            # Check if the user is the owner/author
            if obj.author == request.user:
                return True
            
            # For safe methods, check if the user is a contributor
            project_related = obj.project
            is_contributor = Contributor.objects.filter(user=request.user, project=project_related).exists()
            if request.method in permissions.SAFE_METHODS and is_contributor:
                return True

            return False

        # Logic specific to Project
        if isinstance(obj, Project):
            if obj.author == request.user:
                return True
            return Contributor.objects.filter(user=request.user, project=obj).exists()
        
        # For other objects (like Comments), check the related project's contributors and author
        project_related = obj.project if hasattr(obj, 'project') else obj.issue.project
        if project_related.author == request.user:
            return True
        return Contributor.objects.filter(user=request.user, project=project_related).exists()





class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit or delete it.
    """
    
    def has_object_permission(self, request, view, obj):
        # Permissions are only allowed to the owner of the comment.        
        return obj.author == request.user
    
