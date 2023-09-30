"""
Serializers for the user API view.
"""
# SERIALIZERS: Is the way to convert objects to and \
# from Python objects. It takes in a JSON imput, \
# validates the input (to make sure that it is \
# secure and correct), and then it converts it \
# to either a Python object OR to a model in \
# our Database(!!!)

from django.contrib.auth import (
    get_user_model,
    # F-n comes with Django that allows to authenticate \
    # with authentication system.
    authenticate
)
from django.utils.translation import gettext as _

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object."""

    # Will reuse UserSerializer for both - creating users and updating users.

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

    # Overwriting update method on UserSerializer
    # 'instance' is the model instance that is being updated.
    # 'validated_data' data that was already passed through \
    # serializer validation (in this case 'email', 'password' and 'name').
    def update(self, instance, validated_data):
        """Update and return user."""
        # Setting default value to None.
        # We don't wan't to add password in raw form, \
        # first we want to hash it. Removing password from \
        # the dictionary. Password update is optional therefore \
        # we provide default to 'None'. So if user doesn't provide \
        # the password, it will default to Null(?) value.
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        # Need to return it to be used by View, if required.
        return user


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user auth token."""
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
    )

    def validate(self, attrs):
        """Validate and authenticate the user."""
        # 'attrs' -> atributes
        # Validate method is called on the Serializer on \
        # the validation stage, when it goes to validate the \
        # input to the serializer.
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password,
        )
        if not user:
            msg = _('Unable to authenticate with provided credentials.')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
