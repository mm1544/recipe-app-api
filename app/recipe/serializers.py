"""
Serialoizers for recipe APIs.
"""

from rest_framework import serializers

from core.models import (
    Recipe,
    Tag,
)


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for recipes."""
    # Will be useing ModelSerializer becuase this serializer \
    # represent specific model in the system, which is our \
    # Recipe model.

    class Meta:
        model = Recipe
        fields = ['id', 'title', 'time_minutes', 'price', 'link']
        # Because we don't want user to be able to change DB \
        # id of a recipe.
        read_only_fileds = ['id']


class RecipeDetailSerializer(RecipeSerializer):
    """Serializer for recipe detail view."""
    # We are extending class RecipeSerializer. We will add few \
    # extra fields.

    class Meta(RecipeSerializer.Meta):
        # Using Meta class inside of class RecipeSerializer

        # Adding additional field
        fields = RecipeSerializer.Meta.fields + ['description']


class TagSerializer(serializers.ModelSerializer):
    """Serializer for tags."""

    class Meta:
        model = Tag
        # Fields which we want to convert from Model to serializer.
        fields = ['id', 'name']
        read_only_fields = ['id']
