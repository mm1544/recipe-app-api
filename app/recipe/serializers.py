"""
Serialoizers for recipe APIs.
"""
# SERIALIZERS: Is the way to convert objects to and \
# from Python objects. It takes in a JSON imput, \
# validates the input (to make sure that it is \
# secure and correct), and then it converts it \
# to either a Python object OR to a model in \
# our Database(!!!)

from rest_framework import serializers

from core.models import (
    Recipe,
    Tag,
)


class TagSerializer(serializers.ModelSerializer):
    """Serializer for tags."""
    # Will be using this serializer as nested serializer \
    # in 'RecipeSerializer'.

    class Meta:
        model = Tag
        # Fields which we want to convert from Model to serializer.
        fields = ['id', 'name']
        read_only_fields = ['id']


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for recipes."""
    # Will be useing ModelSerializer becuase this serializer \
    # represent specific model in the system, which is our \
    # Recipe model.

    # It is going to be a list of tags assigned to the recipe.
    # By default nested serialyzers are readonly(!!) therefore we \
    # will be using custom code to change this behaviour.
    tags = TagSerializer(many=True, required=False)

    class Meta:
        model = Recipe
        fields = ['id', 'title', 'time_minutes', 'price', 'link', 'tags']
        # Because we don't want user to be able to change DB \
        # id of a recipe.
        read_only_fileds = ['id']

    def _get_or_create_tags(self, tags, recipe):
        """Handle getting or creating tags as needed."""
        # Because we are doing it in serializer and not the view, we \
        # need to use self.context. The context is passed TO the \
        # serializer BY the view, when you are using serializer for \
        # that particular view.
        auth_user = self.context['request'].user

        # Looping through all the tags that we have pop'ed from \
        # validated_data
        for tag in tags:
            tag_obj, created = Tag.objects.get_or_create(
                user=auth_user,
                # We want to take all the values that are passed-in to the tag.
                **tag,
            )
            recipe.tags.add(tag_obj)

    # Overwriting 'create' method
    def create(self, validated_data):
        """Create a recipe."""
        # Meaning: If 'tags' exist in 'validated_data', remove 'tags' \
        # from validated data and assign it to the variable. If 'tags' \
        # doesn' exist it will defoult to '[]'
        tags = validated_data.pop('tags', [])
        # We have removed 'tags' from 'validated_data' before creating \
        # recipe
        # Tags are expected to be created separately and added as a \
        # relationship to Recipe from many2many field (on Recipe)
        recipe = Recipe.objects.create(**validated_data)

        self._get_or_create_tags(tags, recipe)

        # Need to return the value from 'create' f-n in order for the \
        # rest of funtionality to work.
        return recipe

    def update(self, instance, validated_data):
        """Update recipe."""
        # 'instance' is an existing instance, that we are updating.
        # 'validated_data' is data that we want 'instance' to be updated with.

        tags = validated_data.pop('tags', None)

        if tags is not None:
            # Clears all the existing assigned tags, because we are updating \
            # tags with passed-in tags from 'validated_data'
            instance.tags.clear()
            self._get_or_create_tags(tags, instance)
            # If tags are not provided in 'validated_data', then there is no \
            # need to update them on instance.

        for attr, value in validated_data.items():
            # For the rest of the 'validated_data'. Everything will be assigned \
            # to the instance.
            setattr(instance, attr, value)

        instance.save()
        return instance


class RecipeDetailSerializer(RecipeSerializer):
    """Serializer for recipe detail view."""
    # We are extending class RecipeSerializer. We will add few \
    # extra fields.

    class Meta(RecipeSerializer.Meta):
        # Using Meta class inside of class RecipeSerializer

        # Adding additional field
        fields = RecipeSerializer.Meta.fields + ['description']
