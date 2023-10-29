from django.db import models
from authentication.models import User
import uuid


class Project(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    TYPE_CHOICES = [
        ("backend", "Back-end"),
        ("frontend", "Front-end"),
        ("ios", "iOS"),
        ("android", "Android"),
    ]
    project_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    created_time = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)


class Contributor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)


class Issue(models.Model):
    PRIORITY_CHOICES = [("low", "Low"), ("medium", "Medium"), ("high", "High")]
    STATUS_CHOICES = [
        ("todo", "To Do"),
        ("inprogress", "In Progress"),
        ("finished", "Finished"),
    ]
    TAG_CHOICES = [("bug", "Bug"), ("feature", "Feature"), ("task", "Task")]
    name = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default="todo"
    )
    priority = models.CharField(
        max_length=6, choices=PRIORITY_CHOICES, default="medium"
    )
    tag = models.CharField(max_length=7, choices=TAG_CHOICES)
    created_time = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(
        Project, related_name="issues", on_delete=models.CASCADE
    )
    assignee = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="assigned_issues",
    )


class Comment(models.Model):
    description = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)
    issue = models.ForeignKey(
        Issue, related_name="comments", on_delete=models.CASCADE
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
