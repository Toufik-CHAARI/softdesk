from rest_framework.response import Response
from rest_framework.decorators import api_view
from authentication.models import User
from .serializers import UserSerializer
from rest_framework.viewsets import ModelViewSet


@api_view(['GET'])
def getData(request):
    users = User.objects.all()
    serializer = UserSerializer(users,many=True)
    return Response(serializer.data) 


class userViewset(ModelViewSet):
    
    serializer_class = UserSerializer
    def get_queryset(self): 
        return User.objects.all()
    