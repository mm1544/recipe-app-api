"""
Views for the user API.
"""
from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

# 'UserSerializer' is our custom Serializer.
from user.serializers import (
    UserSerializer,
    AuthTokenSerializer,
)


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system."""
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user."""
    # We are customising a serializer to use our custom \
    # Serializer that we have created. We need to do \
    # this because initially ObtainAuthToken view uses \
    # Username and Password and we want to use Email and Password.
    serializer_class = AuthTokenSerializer
    # It is optional. It makes browsable API for REST \
    # framework, it wouldn't show a nice UI.
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
