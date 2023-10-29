from rest_framework import serializers
from authentication.models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.
    This serializer includes additional validation for age and consent
    fields.It ensures that the user provides values for
    'can_be_contacted' and 'can_data_be_shared' fields.
    It also auto-populates the 'consent_choice' based on
    the consent fields.
    """

    password = serializers.CharField(write_only=True)
    can_be_contacted = serializers.BooleanField(required=True)
    can_data_be_shared = serializers.BooleanField(required=True)

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
            "id"
        ]

    def validate_age(self, value):
        """
        Validate the age of the user.
        Ensures that the provided age is 15 or older.
        """
        if value < 15:
            raise serializers.ValidationError(
                "Users must be 15 years or older."
            )
        return value

    def validate_can_be_contacted(self, value):
        """
        Validate the 'can_be_contacted' field.
        Ensures that a value is provided for the
        'can_be_contacted' field.
        """
        if value is None:
            raise serializers.ValidationError(
                "The can_be_contacted field must be provided."
            )
        return value

    def validate_can_data_be_shared(self, value):
        """
        Validate the 'can_data_be_shared' field.
        Ensures that a value is provided for the
        'can_data_be_shared' field.

        """
        if value is None:
            raise serializers.ValidationError(
                "The can_data_be_shared field must be provided."
            )
        return value

    def validate(self, data):
        """
        Override the default validation.
        This sets the 'consent_choice' to True if either
        'can_be_contacted' or
        'can_data_be_shared' are True.
        """
        if data.get("can_be_contacted") or data.get("can_data_be_shared"):
            data["consent_choice"] = True
        return data

    def create(self, validated_data):
        """
        Create and return a new 'User' instance.
        """
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
