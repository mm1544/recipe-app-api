"""
Database models.
"""
import uuid
import os

from django.conf import settings
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


def recipe_image_file_path(instance, filename):
    """Generate file path for new recipe image."""
    # Function that generates the path to the image that \
    # user uploads.
    # 'instance' is the instance of the object, the image \
    # is being uploaded to.
    # 'filename' - name of the original file that is being \
    # uploaded.
    ext = os.path.splitext(filename)[1]
    # Creating custom filename and appending extension to \
    # the end.
    filename = f'{uuid.uuid4()}{ext}'

    # This ensures that the string is created in the \
    # apropriate format for the operating system that we \
    # arre using. Urls would be different for windows, linux or \
    # mac etc.
    return os.path.join('uploads', 'recipe', filename)


class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user."""
        if not email:
            raise ValueError('User must have an email address.')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create and return a new superuser."""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Recipe(models.Model):
    """Recipe object."""
    # 'AUTH_USER_MODEL' we define in settings.py \
    # We do that so that in every model we use/reference \
    # to the same User Model.
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        # If related onj is deleted, we are going to \
        # cascade this change to this model. So if we \
        # have a user with a multiple recipes, and that \
        # user removes its profile, then it is going to \
        # delete all(!) the Recipes asociated to the user.
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    time_minutes = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    link = models.CharField(max_length=255, blank=True)
    # 'ManyToManyField' - because we can have many diferent \
    # recipes that can have many diferent tags.
    tags = models.ManyToManyField('Tag')
    ingredients = models.ManyToManyField('Ingredient')
    # 'recipe_image_file_path' is a reference to the f-n that \
    # generates the filepath. That is Django way to do it.
    image = models.ImageField(null=True, upload_to=recipe_image_file_path)

    def __str__(self):
        # It defines how object should be displayed in Dj Admin.
        return self.title


class Tag(models.Model):
    """Tag for filtering recipes."""
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        # Meaning: If the user is deleted, then Tag will be \
        # deleted as well.
        on_delete=models.CASCADE,
    )

    # Defining string representation of the Tag
    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Ingredient for recipes."""
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        # String representation
        return self.name
