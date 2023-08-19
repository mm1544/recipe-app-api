"""
Views for the user API.
"""
from rest_framework import generics

# 'UserSerializer' is our custom Serializer.
from user.serializers import UserSerializer


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system."""
    serializer_class = UserSerializer
