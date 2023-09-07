"""
Views for the recipie APIs.
"""

from rest_framework import (
    viewsets,
    # Thing which can be mixed in into view to add \
    # aditional functionality.
    mixins,
)

from rest_framework.authentication import TokenAuthentication
# That is the permission that we want to check before users \
# can use recipe endpoint.
from rest_framework.permissions import IsAuthenticated

from core.models import (
    Recipe,
    Tag,
)
from recipe import serializers


class RecipeViewSet(viewsets.ModelViewSet):
    """View for manage recipe APIs."""
    # ViewSet will generate a multiple endpoints e.g. 'list', \
    # 'id' and it will have an ability to pergorm a multiple \
    # different methods.

    serializer_class = serializers.RecipeDetailSerializer
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

    # Overwriting method

    def get_serializer_class(self):
        """REturn the serializer class for request."""
        if self.action == 'list':
            # If we are calling 'list' endpoint, which \
            # is HTTP GET to the Root of a API, it will 'come-up' as \
            # the action 'list'(??). It will return serializer for \
            # the list view (find-of preview serializer). Othervise \
            # it will return 'serializer_class'
            # NOT adding here '()' because we want to return a reference \
            # to the class, but not the obj of a class.
            return serializers.RecipeSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new recipr."""
        # Overwriting the behaviour for when DJ framework saves the model \
        # in the viewset.
        # Meaning of this method: When we perform creation of a new object \
        # through this model viewset(?), so when we create a new recipe, \
        # through 'create_feature'(?) of the viewset, then we will call \
        # method 'perform_create' as part of that model creation. \
        # It accept 'serializer' and it should be a walidated serializer.
        # And will set 'user' to the current authenticated user, when we \
        # save the object.
        serializer.save(user=self.request.user)


class TagViewSet(mixins.DestroyModelMixin,
                 mixins.UpdateModelMixin,
                 mixins.ListModelMixin,
                 viewsets.GenericViewSet):
    # 'ListModelMixin' allows adding listing functionality \
    # for listing models.
    # 'viewsets' allows to use CRUD functionality out of the box.
    # 'GenericViewSet' allows throwing mixsins, so that you can have a mixin functionality that you desire for your particular API.
    """Manage tags in the database."""
    serializer_class = serializers.TagSerializer
    queryset = Tag.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    # Need to overwrite get_queryset method (coms with viewset), \
    # to make sure it returns only the queryset objects for \
    # the authenticated users. By default it would return ALL \
    # the diferent tags that exist in the database. We want to \
    # filter them to the user that created them.
    def get_queryset(self):
        """Filter queryset to authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-name')
