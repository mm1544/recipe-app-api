"""Tests for recipe APIs."""
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Recipe

from recipe.serializers import (
    # Will give recipe preview/listing
    RecipeSerializer,
    # It will give details for particular recipe
    RecipeDetailSerializer,
)

# Gives a recipe url
RECIPIES_URL = reverse('recipe:recipe-list')


def detail_url(recipe_id):
    """Create and return a recipe detail URL."""
    # We need to pass-in recipe id into url. Each detail URL \
    # will be different.
    return reverse('recipe:recipe-detail', args=[recipe_id])


def create_recipe(user, **params):
    """Create and return a sample recipe."""
    defaults = {
        'title': 'Sample recipe title',
        'time_minutes': 22,
        'price': Decimal('5.25'),
        'description': 'Sample description',
        'link': 'http://example.com/recipe.pdf',
    }
    defaults.update(params)

    recipe = Recipe.objects.create(user=user, **defaults)
    return recipe

# There will be 2 types of tests 1)Authenticated and 2)Unauthenticated


class PublicRecipeAPITests(TestCase):
    """Test unauthenticated API requests."""

    # Recipies can be retrieved by the User when they are authenticated. Recipies will be not public. Only loged-in users will be allowed to see recipies wich they stored in recipe-book.

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API."""
        res = self.client.get(RECIPIES_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeApiTests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'user@example.com',
            'testpass123',
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_recipes(self):
        """Test retrieving a list of recipes."""
        create_recipe(user=self.user)
        create_recipe(user=self.user)

        # It should return the recipies, for certain user, that we have on the system.
        res = self.client.get(RECIPIES_URL)

        # Recipies in reverse order
        recipes = Recipe.objects.all().order_by('-id')
        # We expect 'res' to match whatever 'serializer' returns.
        serializer = RecipeSerializer(recipes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # Checking if 'res.data' dictionary that is returned in \
        # response, is equal to 'serializer.data'.
        # SO 'serializer.data' is the dictionary of the objects \
        # that are passed through Serializer.
        self.assertEqual(res.data, serializer.data)

    def test_recipe_list_limited_to_user(self):
        """Test list of recipes is limited to authenticated user."""
        other_user = get_user_model().objects.create_user(
            'other@example.com',
            'password123',
        )
        create_recipe(user=other_user)
        # Recipe for the authenticated user, created in 'setUp' method.
        create_recipe(user=self.user)

        res = self.client.get(RECIPIES_URL)

        # Filter recipes just from the authenticated user
        recipes = Recipe.objects.filter(user=self.user)
        # 'many=True' to be able to pass-in(?) many
        serializer = RecipeSerializer(recipes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_get_recipe_detail(self):
        """Test get recipe detail."""
        recipe = create_recipe(user=self.user)

        url = detail_url(recipe.id)
        res = self.client.get(url)

        # It is just one recipe so we don't pass-in many=True
        serializer = RecipeDetailSerializer(recipe)
        self.assertEqual(res.data, serializer.data)

    def test_create_recipe(self):
        """Test creating a recipe."""
        # Not using 'create_recipe' helper f-n because the whole \
        # pont of this test is creating recipe through API.

        # Will pass a payload through API with the content of \
        # a recipe. We want to ensure that the recipe was \
        # created successfuly and corectly in the database.
        payload = {
            'title': 'Sample recipe',
            'time_minutes': 30,
            'price': Decimal('5.99'),
        }
        res = self.client.post(RECIPIES_URL, payload)  # /api/recipies/recipe

        # 201 - created HTTP responce code.
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=res.data['id'])
        # It will iterate trough payload and 'k' will be key, and 'v' will \
        # be value.
        for k, v in payload.items():
            # 'getattr'(!) - Python f-n. It allows to get an attribute without using \
            # 'dot' notation(!!!).
            self.assertEqual(getattr(recipe, k), v)
        self.assertEqual(recipe.user, self.user)
