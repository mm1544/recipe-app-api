"""
Database models.
"""
from django.conf import settings
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


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
        # have a user with a multiple recipies, and that \
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
    """Ingredient for recipies."""
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        # String representation
        return self.name
