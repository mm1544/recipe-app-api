"""
Serializers for the user API view.
"""
# SERIALIZERS: Is the way to convert objects to and \
# from Python objects. It takes in a JSON imput, \
# validates the input (to make sure that it is \
# secure and correct), and then it converts it \
# to either a Python object OR to a model in \
# our Database(!!!)

from django.contrib.auth import get_user_model
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object."""

    # Telling to Dj REST framework the model and fields, \
    # and additional arguments that we want to pass \
    # to Serializer. Serializer needs to know which \
    # model it is representing.
    class Meta:
        model = get_user_model()
        # Fields that we want to enable for the Serializer.
        fields = ['email', 'password', 'name']
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    # Allows to OVERWRITE the behaviour that Serializer \
    # does when you create new objects out of that \
    # Serializer. Default behaviour is to create \
    # an object with just whatever values are passed in.
    # This 'create' method will be called after the \
    # (input) validation and ONLY will be called if \
    # the validation is successful.
    def create(self, validated_data):
        """Create and return a user with encrypted password."""
        return get_user_model().objects.create_user(**validated_data)
