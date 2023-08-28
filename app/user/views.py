"""
Views for the user API.
"""
from rest_framework import generics, authentication, permissions
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


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user."""
    # Using the same serializer as 'CreateUserView'
    serializer_class = UserSerializer
    # In Dj REST authentication is split into 2:
    # 1)Authentication -> How do you know the user is the user \
    # they say they are. For this purpose we use Token authentication.
    # 2)Permission_classes -> We already know who this User is, \
    # but now we need to know what this particular usr is allowed to do.
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    # Overwriting 'get_object' method, and we retrieving the \
    # user that is attached to the request.
    # We will use it to return the User obj for the request, made \
    # for this API. So when do you make http GET request for this \
    # endpoint, it is going to call 'get_object' fto get the user. \
    # Then it will return the user that is authenticated, and it \
    # will run it hrough the serializer, before returning the result \
    # to the API.
    def get_object(self):
        """Retrieve and return the authenticated user."""
        return self.request.user
