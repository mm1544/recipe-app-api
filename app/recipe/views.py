"""
Views for the recipe APIs.
"""
from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiParameter,
    OpenApiTypes,
)

from rest_framework import (
    viewsets,
    # Thing which can be mixed in into view to add \
    # aditional functionality.
    mixins,
    status,
)

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
# That is the permission that we want to check before users \
# can use recipe endpoint.
from rest_framework.permissions import IsAuthenticated

from core.models import (
    Recipe,
    Tag,
    Ingredient,
)
from recipe import serializers


@extend_schema_view(
    # To customise automated documentation
    list=extend_schema(
        # Extending schema for 'list' endpoint
        parameters=[
            OpenApiParameter(
                'tags',
                OpenApiTypes.STR,
                description='Comma separated list of IDs to filter'
            ),
            OpenApiParameter(
                'ingredients',
                OpenApiTypes.STR,
                description='Comma separated list of ingredient IDs to filter',
            )
        ]
    )
)
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

    def _params_to_ints(self, qs):
        """Convert a list of strings to integers."""
        # 'qs' is a string e.g. '1,2,3'
        return [int(str_id) for str_id in qs.split(',')]

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
        tags = self.request.query_params.get('tags')
        ingredients = self.request.query_params.get('ingredients')
        queryset = self.queryset
        if tags:
            tag_ids = self._params_to_ints(tags)
            queryset = queryset.filter(tags__id__in=tag_ids)
        if ingredients:
            ingredient_ids = self._params_to_ints(ingredients)
            queryset = queryset.filter(ingredients__id__in=ingredient_ids)

        # Using 'distinct()' becuase can get duplicate results if you have \
        # multiple recipies assigned to the same tag or ingredient.
        return queryset.filter(
            user=self.request.user
        ).order_by('-id').distinct()

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
        elif self.action == 'upload_image':
            # 'upload_image' is a custom action that we will define in \
            # recipeviewset. 'actions' is the way you can add aditional \
            # functionality on top of the viewset default functionality. 'ModelViewSet' provides multiple default actions (refere to decumentation) - E.g. 'list', 'delete', 'update'. We will add a custom action 'upload_image'. We need to get a special serializer for calling this action.
            return serializers.RecipeImageSerializer

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

    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        """Upload an image to recipe."""
        # Adding custom action.
        # 'detail=True' meaning: there is a specific id of recipe. Non-detail \
        # veiw is just a list-view, that has a generic list of all the \
        # recipies.
        # We ant to apply this custom action just to detail endpoint (specific \
        # recipe must be provided).
        # 'url_path='upload-image'' - lets us specify a custom url path for our \
        # action.
        recipe = self.get_object()
        # Passing in the data that was posted
        serializer = self.get_serializer(recipe, data=request.data)

        if serializer.is_valid():
            # Will save the imahe to the database.
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        # Executed when serializer is not valid and we return errors.
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema_view(
    # Updating automated documentation for list method for both views that are inheriting from this BaseRecipeAttrViewSet.
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                # Defining parameter. Parameter type is Int.
                'assigned_only',
                OpenApiTypes.INT,
                # Enumerator allows to define specific values \
                # of parameter.
                enum=[0, 1],
                description='Filter by items assigned to recipes.'
            )
        ]
    )
)
class BaseRecipeAttrViewSet(mixins.DestroyModelMixin,
                            mixins.UpdateModelMixin,
                            mixins.ListModelMixin,
                            viewsets.GenericViewSet):
    """Base viewset for recipe attributes."""
    # 'base' - because will use it as base class for other viewsets.
    # 'RecipeAttr' - 'mixins.DestroyModelMixin' and etc. are Recipe \
    # attributes

    # Adds support for using token authentication.
    authentication_classes = [TokenAuthentication]
    # Meaning: All users should be authenticated to use this endpoint.
    permission_classes = [IsAuthenticated]

    # Need to overwrite get_queryset method (coms with viewset), \
    # to make sure it returns only the queryset objects for \
    # the authenticated users. By default it would return ALL \
    # the diferent tags that exist in the database. We want to \
    # filter them to the user that created them.
    def get_queryset(self):
        """Filter queryset to authenticated user."""
        # 'bool' f-n converts integer to bool
        assigned_only = bool(
            # When calling .get() we specify a default value of \
            # 0 for case when 'assigned_only' is not passed-in.
            int(self.request.query_params.get('assigned_only', 0))
        )
        queryset = self.queryset
        if assigned_only:
            # 'distinct()' will ensure that returned values are \
            # unique.
            queryset = queryset.filter(recipe__isnull=False)
        return queryset.filter(
            user=self.request.user
        ).order_by('-name').distinct()


class TagViewSet(BaseRecipeAttrViewSet):
    # 'ListModelMixin' allows adding listing functionality \
    # for listing models.
    # 'viewsets' allows to use CRUD functionality out of the box.
    # 'GenericViewSet' allows throwing mixsins, so that you can have a mixin functionality that you desire for your particular API.
    """Manage tags in the database."""
    serializer_class = serializers.TagSerializer
    queryset = Tag.objects.all()


class IngredientViewSet(BaseRecipeAttrViewSet):
    """Manage ingredients in the database."""
    # 'mixins.UpdateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet' \
    # - inherited base classes.
    serializer_class = serializers.IngredientSerializer
    # Sets queryset to the Ingredient objects. It tells Dj what models we \
    # want to be manageble throught the  viewset.
    queryset = Ingredient.objects.all()
    # Now will hook this viewset to the URL.
