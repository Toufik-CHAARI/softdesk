from rest_framework import viewsets
from .models import Project, Contributor, Issue, Comment
from .serializers import (
    ProjectSerializer,
    ContributorSerializer,
    IssueSerializer,
    CommentSerializer,
)
from rest_framework.permissions import IsAuthenticated
from .permissions import (
    IsOwner,
    IsProjectContributorOrAuthorOrSuperuser,
)
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from rest_framework.exceptions import PermissionDenied
from django.core.exceptions import ValidationError
from rest_framework import serializers


class ProjectViewSet(viewsets.ModelViewSet):
    """
    ViewSet for the Project model.
    Handles CRUD operations for projects by ensuring that:
    - Only the authenticated user, owner, contributor, author
    or superuser can access or modify the data.
    - The author of a project cannot be altered during update operations.

    """

    permission_classes = [
        IsAuthenticated,
        IsOwner,
        IsProjectContributorOrAuthorOrSuperuser,
    ]
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Project.objects.all()
        return Project.objects.filter(
            Q(author=self.request.user)
            | Q(contributor__user=self.request.user)
        ).distinct()

    def perform_update(self, serializer):
        # Ensure the author is not changed.
        if "author" in serializer.validated_data:
            del serializer.validated_data["author"]

        super(ProjectViewSet, self).perform_update(serializer)

    def perform_create(self, serializer):
        project = serializer.save(author=self.request.user)

        if self.request.user.is_superuser:
            Contributor.objects.create(user=self.request.user, project=project)


class ContributorViewSet(viewsets.ModelViewSet):
    """
    ViewSet for the Contributor model.
    Manages CRUD operations for contributors by ensuring that:
    - Only the authenticated user, owner, contributor, author
    or superuser can add a contributor.

    """

    permission_classes = [
        IsAuthenticated,
        IsOwner,
        IsProjectContributorOrAuthorOrSuperuser,
    ]
    queryset = Contributor.objects.all()
    serializer_class = ContributorSerializer

    def create(self, request, *args, **kwargs):
        project_id = request.data.get("project")

        if not project_id:
            return Response(
                {"detail": "A project must be specified."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        project = Project.objects.get(id=project_id)

        # Check if user is the author
        if project.author == request.user:
            return super(ContributorViewSet, self).create(
                request, *args, **kwargs
            )
        # Check if user is a contributor
        if Contributor.objects.filter(
            user=request.user, project=project
        ).exists():
            return super(ContributorViewSet, self).create(
                request, *args, **kwargs
            )
        # Check if user is a superuser
        if request.user.is_superuser:
            return super(ContributorViewSet, self).create(
                request, *args, **kwargs
            )

        return Response(
            {"detail": "You don't have the permissions to add a contributor."},
            status=status.HTTP_403_FORBIDDEN,
        )


class IssueViewSet(viewsets.ModelViewSet):
    """
    ViewSet for the Issue model.
    Handles CRUD operations for issues by ensuring that:
    - Only authenticated users who are contributors, authors, or
    superusers can access or modify the data.
    - During creation, the specified project exists.
    - The assignee is validated as a contributor or author of the project.
    """

    permission_classes = [
        IsAuthenticated,
        IsProjectContributorOrAuthorOrSuperuser,
    ]
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def create(self, request, *args, **kwargs):
        project_id = request.data.get("project")
        if not Project.objects.filter(id=project_id).exists():
            return Response(
                {"detail": "The specified project does not exist."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # If an assignee is provided during creation
        assignee_id = request.data.get("assignee")
        if assignee_id:
            project = Project.objects.get(id=project_id)
            if (
                not project.author.id == int(assignee_id)
                and not Contributor.objects.filter(
                    user_id=assignee_id, project=project
                ).exists()
            ):
                error_detail = (
                    "The assignee must be a contributor "
                    "or the author of the project."
                )
                return Response(
                    {"detail": error_detail},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        return super(IssueViewSet, self).create(request, *args, **kwargs)

    def perform_update(self, serializer):
        # If an assignee is provided during update
        assignee = serializer.validated_data.get("assignee", None)
        if assignee:
            project = self.get_object().project
            if (
                not project.author.id == assignee.id
                and not Contributor.objects.filter(
                    user=assignee, project=project
                ).exists()
            ):
                error_message = (
                    "The assignee must be a contributor "
                    "or the author of the project."
                )
                raise serializers.ValidationError({"assignee": error_message})

        serializer.save()

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Issue.objects.all()
        user_projects = Project.objects.filter(
            Q(author=self.request.user)
            | Q(contributor__user=self.request.user)
        ).distinct()
        # Return issues only from those projects
        return Issue.objects.filter(project__in=user_projects)


class CommentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for the Comment model.

    Manages CRUD operations for comments. It ensures that:
    - Only authenticated users who are contributors, authors,
    or superusers can create comments.
    - Comments are associated with valid issues.
    - The comment's author must be a contributor
    or the author of the associated project.

    """

    permission_classes = [
        IsAuthenticated,
        IsOwner,
        IsProjectContributorOrAuthorOrSuperuser,
    ]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        issue_id = self.request.data.get("issue")

        if not issue_id:
            raise ValidationError(
                "The 'issue' key is required in the request data."
            )

        try:
            issue_related_project = Issue.objects.get(id=issue_id).project
        except Issue.DoesNotExist:
            raise ValidationError(f"Issue with ID {issue_id} does not exist.")

        if not (
            issue_related_project.author == self.request.user
            or Contributor.objects.filter(
                user=self.request.user, project=issue_related_project
            ).exists()
        ):
            error_msg = (
                "You must be a contributor or the author "
                "of the project to create a comment."
            )

            raise PermissionDenied(error_msg)

        serializer.save(
            author=self.request.user,
            issue=Issue.objects.get(id=self.request.data["issue"]),
        )

    def get_queryset(self):
        # Get projects where the user is a contributor or author
        if self.request.user.is_superuser:
            return Comment.objects.all()
        user_projects = Project.objects.filter(
            Q(author=self.request.user)
            | Q(contributor__user=self.request.user)
        ).distinct()
        # Return comments only from issues of those projects
        return Comment.objects.filter(issue__project__in=user_projects)
