"""
Views for the recipie APIs.
"""

from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
# That is the permission that we want to check before users \
# can use recipe endpoint.
from rest_framework.permissions import IsAuthenticated

from core.models import Recipe
from recipe import serializers


class RecipeViewSet(viewsets.ModelViewSet):
    """View for manage recipe APIs."""
    # ViewSet will generate a multiple endpoints e.g. 'list', \
    # 'id' and it will have an ability to pergorm a multiple \
    # different methods.

    serializer_class = serializers.RecipeSerializer
    # 'queryset' represents the objects that are available for \
    # this viewset. Because it is a model viewset, it is expected \
    # to work with a model, and when you tell which models to use, \
    # you specify a 'queryset'. So it is a 'queryset' of objects \
    # that will be manageble through this API.
    queryset = Recipe.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    # We want to make sure that Recipes are filtered to the \
    # authenticated user. We will achieve that by overwriting \
    # get_queryset method
    def get_queryset(self):
        """Retrieve recipes for authenticated user."""
        # 'queryset' here is defined in the same class, on line \
        # "queryset = Recipe.objects.all()".
        # All users that uses API must be authenticated, so we can \
        # retrieve 'user' obj from 'request' that is passed in by \
        # the authentication system.
        return self.queryset.filter(user=self.request.user).order_by('-id')
