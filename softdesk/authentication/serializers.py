from rest_framework import serializers
from authentication.models import User


class UserSerializer(serializers.ModelSerializer):
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
        ]
    
    def validate_age(self, value):
        if value < 15:
            raise serializers.ValidationError(
                "Users must be 15 years or older."
            )
        return value
    
    def validate_can_be_contacted(self, value):        
        if value is None:            
            raise serializers.ValidationError(
                "The can_be_contacted field must be provided."
            )
        return value

    def validate_can_data_be_shared(self, value):
        if value is None:
            raise serializers.ValidationError(
                "The can_data_be_shared field must be provided."
            )
        return value

    def validate(self, data):
        # If either 'can_be_contacted' or 'can_data_be_shared' is True, 
        # then 'consent_choice' is automatically set to True.
        if data.get('can_be_contacted') or data.get('can_data_be_shared'):
            data['consent_choice'] = True
        return data
    

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
