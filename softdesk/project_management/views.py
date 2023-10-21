from rest_framework import viewsets
from .models import Project, Contributor, Issue, Comment
from .serializers import ProjectSerializer, ContributorSerializer, IssueSerializer, CommentSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwner,IsProjectContributorOrAuthor
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from authentication.models import User
from rest_framework.exceptions import PermissionDenied

class ProjectViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated,IsOwner,IsProjectContributorOrAuthor]
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    def get_queryset(self):
    # Return projects where the user is the author or a contributor.
        return Project.objects.filter(Q(author=self.request.user) | Q(contributor__user=self.request.user)).distinct()
    def perform_update(self, serializer):
        # Ensure the author is not changed.
        if 'author' in serializer.validated_data:
            del serializer.validated_data['author']
        
        super(ProjectViewSet, self).perform_update(serializer)
    

class ContributorViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Contributor.objects.all()
    serializer_class = ContributorSerializer
    


class IssueViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated,IsOwner,IsProjectContributorOrAuthor]
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    def create(self, request, *args, **kwargs):
        project_id = request.data.get('project')
        if not Project.objects.filter(id=project_id).exists():
            return Response({"detail": "The specified project does not exist."}, status=status.HTTP_400_BAD_REQUEST)
        return super(IssueViewSet, self).create(request, *args, **kwargs)
    def get_queryset(self):
        # Get projects where the user is a contributor or author
        user_projects = Project.objects.filter(Q(author=self.request.user) | Q(contributor__user=self.request.user)).distinct()
        # Return issues only from those projects
        return Issue.objects.filter(project__in=user_projects) 

class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated,IsOwner,IsProjectContributorOrAuthor]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    
    def perform_create(self, serializer):
        issue_related_project = Issue.objects.get(id=self.request.data['issue']).project
        if not (issue_related_project.author == self.request.user or Contributor.objects.filter(user=self.request.user, project=issue_related_project).exists()):
            raise PermissionDenied("You must be a contributor or the author of the project to create a comment.")
        
        serializer.save(author=self.request.user)

    def get_queryset(self):
        # Get projects where the user is a contributor or author
        user_projects = Project.objects.filter(Q(author=self.request.user) | Q(contributor__user=self.request.user)).distinct()
        # Return comments only from issues of those projects
        return Comment.objects.filter(issue__project__in=user_projects)

