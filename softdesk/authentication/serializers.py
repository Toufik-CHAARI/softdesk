from rest_framework import serializers
from authentication.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta :
        model = User
        #fields = '__all__'
        fields = ['username', 'age', 'consent_choice', 'can_be_contacted', 'can_data_be_shared','first_name', 'last_name']