"""
Serialoizers for recipe APIs.
"""

from rest_framework import serializers

from core.models import Recipe


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
