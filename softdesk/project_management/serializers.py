from rest_framework import serializers
from .models import Project, Contributor, Issue, Comment
from authentication.models import User


class ProjectSerializer(serializers.ModelSerializer):
    """
    Serializer for the Project model.
    This serializer enables to serialize and deserialize
    `Project` objects.It ensures the author of a project
    cannot be altered during an update operation.
    """

    class Meta:
        model = Project
        fields = "__all__"

    def update(self, instance, validated_data):
        if "author" in validated_data:
            raise serializers.ValidationError(
                {"author": "You cannot change the author of the project."}
            )

        return super(ProjectSerializer, self).update(instance, validated_data)


class ContributorSerializer(serializers.ModelSerializer):
    """
    Serializer for the Contributor model.
    Enables serialization and deserialization for `Contributor` objects
    without additional custom logic.
    """

    class Meta:
        model = Contributor
        fields = "__all__"


class IssueSerializer(serializers.ModelSerializer):
    """
    Serializer for the Issue model.
    Enables basic serialization and deserialization as well as:
    - Validates the existence of a related project.
    - Prevents alteration of the issue's author on update.
    """

    assignee = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), required=False
    )

    def validate_project(self, value):
        if not Project.objects.filter(id=value.id).exists():
            raise serializers.ValidationError(
                "The specified project does not exist."
            )
        return value

    class Meta:
        model = Issue
        fields = "__all__"

    def update(self, instance, validated_data):
        # Remove the 'author' field to ensure it doesn't get updated
        validated_data.pop("author", None)
        return super(IssueSerializer, self).update(instance, validated_data)


class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer for the Comment model.
    Enables basic serialization and deserialization and provide
    features include:
    - A hyperlinked field to relate to the associated issue.
    - Custom update logic to ensure the comment's author can't be altered.
    """

    issue = serializers.HyperlinkedRelatedField(
        view_name="issue-detail", read_only=True
    )

    class Meta:
        model = Comment
        fields = "__all__"

    def update(self, instance, validated_data):
        # Check if author is trying to be changed
        if (
            "author" in validated_data
            and instance.author != validated_data["author"]
        ):
            raise serializers.ValidationError(
                "The author of the comment cannot be changed."
            )

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance
