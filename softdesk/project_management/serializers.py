from rest_framework import serializers
from .models import Project, Contributor, Issue, Comment

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'
    def update(self, instance, validated_data):
        if 'author' in validated_data:
            raise serializers.ValidationError({"author": "You cannot change the author of the project."})
        
        return super(ProjectSerializer, self).update(instance, validated_data)  
        

class ContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributor
        fields = '__all__'

class IssueSerializer(serializers.ModelSerializer):
    def validate_project(self, value):
        if not Project.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("The specified project does not exist.")
        return value    
    class Meta:
        model = Issue
        fields = '__all__'
    def update(self, instance, validated_data):
        # Remove the 'author' field to ensure it doesn't get updated
        validated_data.pop('author', None)
        return super(IssueSerializer, self).update(instance, validated_data)
        
    

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
    def update(self, instance, validated_data):
        # Check if author is trying to be changed
        if 'author' in validated_data and instance.author != validated_data['author']:
            raise serializers.ValidationError("The author of the comment cannot be changed.")
        
        # For other fields, you can use the usual update logic
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance
