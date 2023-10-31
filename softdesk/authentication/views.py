from rest_framework import status
from rest_framework.status import (
    HTTP_404_NOT_FOUND,
)
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .permissions import IsSuperuserOrSelf
from authentication.models import User
from .serializers import UserSerializer


@api_view(["GET"])
@permission_classes((IsAuthenticated, IsSuperuserOrSelf))
def getUserData(request):
    """
    Retrieve a list of all users for a superuser or the data of the
    authenticated user.If the authenticated user is a superuser,
    returns the data for all users.Otherwise, returns only
    the data for the authenticated user.
    """
    if request.user.is_superuser:
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
    else:
        serializer = UserSerializer(request.user)

    return Response(serializer.data)


@api_view(["GET", "PUT", "DELETE"])
@permission_classes((IsAuthenticated, IsSuperuserOrSelf))
def user_detail(request, user_id=None):
    """
    Retrieve, update, or delete a user by ID.
    Only a superuser or the authenticated user (if they match the user_id)
    can access or modify the user data.

    Args:
    - user_id (int, optional): The ID of the user in order to retrieve,
    update, or delete.

    """
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=HTTP_404_NOT_FOUND)

    if not request.user.is_superuser and request.user != user:
        return Response(
            {"error": "You do not have permission to perform this action."},
            status=status.HTTP_403_FORBIDDEN,
        )

    if request.method == "GET":
        serializer = UserSerializer(user)
        return Response(serializer.data)

    elif request.method == "PUT":
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["POST"])
def register(request):
    """
    Register a new user.
    This view handles user registration by validating and saving
    the provided user data.
    """
    
    if request.method == "POST":
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                return Response(status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
