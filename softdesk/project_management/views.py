from rest_framework import viewsets
from .models import Project, Contributor, Issue, Comment
from .serializers import ProjectSerializer, ContributorSerializer, IssueSerializer, CommentSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwner,IsProjectContributorOrAuthorOrSuperuser
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from authentication.models import User
from rest_framework.exceptions import PermissionDenied
from django.core.exceptions import ValidationError
from rest_framework import serializers

class ProjectViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated,IsOwner,IsProjectContributorOrAuthorOrSuperuser]
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    def get_queryset(self):    
        return Project.objects.filter(Q(author=self.request.user) | Q(contributor__user=self.request.user)).distinct()
    def perform_update(self, serializer):
        # Ensure the author is not changed.
        if 'author' in serializer.validated_data:
            del serializer.validated_data['author']
        
        super(ProjectViewSet, self).perform_update(serializer)
    def perform_create(self, serializer):
        
        project = serializer.save(author=self.request.user)  
        
        if self.request.user.is_superuser:
            Contributor.objects.create(user=self.request.user, project=project)

class ContributorViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Contributor.objects.all()
    serializer_class = ContributorSerializer
    
from rest_framework import serializers

class IssueViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsProjectContributorOrAuthorOrSuperuser]
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def create(self, request, *args, **kwargs):
        project_id = request.data.get('project')
        if not Project.objects.filter(id=project_id).exists():
            return Response({"detail": "The specified project does not exist."}, status=status.HTTP_400_BAD_REQUEST)
        
        # If there's an assignee provided during creation
        assignee_id = request.data.get('assignee')
        if assignee_id:
            project = Project.objects.get(id=project_id)
            if not project.author.id == int(assignee_id) and not Contributor.objects.filter(user_id=assignee_id, project=project).exists():
                return Response({"detail": "The assignee must be a contributor or the author of the project."}, status=status.HTTP_400_BAD_REQUEST)
        
        return super(IssueViewSet, self).create(request, *args, **kwargs)

    def perform_update(self, serializer):
        # If there's an assignee provided during update
        assignee = serializer.validated_data.get('assignee', None)
        if assignee:
            project = self.get_object().project
            if not project.author.id == assignee.id and not Contributor.objects.filter(user=assignee, project=project).exists():
                raise serializers.ValidationError({"assignee": "The assignee must be a contributor or the author of the project."})

        serializer.save()

    def get_queryset(self):
        # Get projects where the user is a contributor or author
        user_projects = Project.objects.filter(Q(author=self.request.user) | Q(contributor__user=self.request.user)).distinct()
        # Return issues only from those projects
        return Issue.objects.filter(project__in=user_projects)





class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated,IsOwner,IsProjectContributorOrAuthorOrSuperuser]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    
    
    def perform_create(self, serializer):
        issue_id = self.request.data.get('issue')
        
        if not issue_id:
            raise ValidationError("The 'issue' key is required in the request data.")
        
        try:
            issue_related_project = Issue.objects.get(id=issue_id).project
        except Issue.DoesNotExist:
            raise ValidationError(f"Issue with ID {issue_id} does not exist.")
        
        if not (issue_related_project.author == self.request.user or Contributor.objects.filter(user=self.request.user, project=issue_related_project).exists()):
            raise PermissionDenied("You must be a contributor or the author of the project to create a comment.")
        
        serializer.save(author=self.request.user,issue=Issue.objects.get(id=self.request.data['issue']))
    
    def get_queryset(self):
        # Get projects where the user is a contributor or author
        user_projects = Project.objects.filter(Q(author=self.request.user) | Q(contributor__user=self.request.user)).distinct()
        # Return comments only from issues of those projects
        return Comment.objects.filter(issue__project__in=user_projects)

