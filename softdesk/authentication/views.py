from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_200_OK

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .permissions import IsSuperuserOrSelf
from rest_framework.authtoken.models import Token
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_200_OK

from authentication.models import User
from .serializers import UserSerializer
from rest_framework.viewsets import ModelViewSet

@api_view(['GET'])
@permission_classes((IsAuthenticated,IsSuperuserOrSelf ))
def getUserData(request):
    if request.user.is_superuser:
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
    else:
        serializer = UserSerializer(request.user)

    return Response(serializer.data)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((IsAuthenticated, IsSuperuserOrSelf))
def user_detail(request, user_id=None):
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=HTTP_404_NOT_FOUND)

    # Check permissions
    if not request.user.is_superuser and request.user != user:
        return Response({"error": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    
    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=HTTP_400_BAD_REQUEST)
    
    user = authenticate(username=username, password=password)
    
    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=HTTP_404_NOT_FOUND)
    
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key},
                    status=HTTP_200_OK)
    
@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def logout(request):
    # Remove the authentication token
    return Response({"detail": "Successfully logged out"}, status=HTTP_200_OK)



@api_view(['POST'])
def register(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)