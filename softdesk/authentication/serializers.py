from rest_framework import serializers
from authentication.models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "username",
            "password",
            "age",
            "consent_choice",
            "can_be_contacted",
            "can_data_be_shared",
            "first_name",
            "last_name",
        ]

    def validate_age(self, value):
        if value < 15:
            raise serializers.ValidationError(
                "Users must be 15 years or older."
            )
        return value

    def create(self, validated_data):
        user = User(
            username=validated_data["username"],
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", ""),
            age=validated_data.get("age"),
            consent_choice=validated_data.get("consent_choice"),
            can_be_contacted=validated_data.get("can_be_contacted"),
            can_data_be_shared=validated_data.get("can_data_be_shared"),
        )
        user.set_password(validated_data["password"])
        user.save()
        return user
