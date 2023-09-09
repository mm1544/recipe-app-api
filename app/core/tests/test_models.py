"""
Tests for models.
"""
# To store one of the values of Recipe object
from decimal import Decimal

from django.test import TestCase
# 'get_user_model' -> to get reference to the default \
# User model from the project.
from django.contrib.auth import get_user_model

from core import models


def create_user(email='user@example.com', password='testpass123'):
    """Create and returna new user."""
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):
    """Test models."""

    def test_create_user_with_email_successful(self):
        """Test creating a user with an email is successful."""
        email = 'test@example.com'
        password = 'testpass123'
        # 'objects' -> referes to the manager that we are going to create.
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test email is normalized for new users."""

        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            # (1)Test2 -> can be capitalized
            # (2)@example.com -> can't be capitalized
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.com', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com'],
        ]

        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, 'sample123')
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """Test that creating a user without an email raises a ValueError."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'test123')

    def test_create_superuser(self):
        """Test creating a superuser."""
        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'test123',
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_recipe(self):
        """Test creating a recipe is successful."""
        # User that will be assigned to the recipe object.
        user = get_user_model().objects.create_user(
            'test@example.com',
            'testpass123',
        )
        recipe = models.Recipe.objects.create(
            # Authenticated user
            user=user,
            title='Sample recipe name',
            # Estimated time to make the recipe
            time_minutes=5,
            price=Decimal('5.50'),
            description='Sample recipe description.',
        )

        # We will add a logic that returns a Title, wen you \
        # require a string representation of a 'recipe'
        self.assertEqual(str(recipe), recipe.title)

    def test_create_tag(self):
        """Test creating a tag is successful."""
        user = create_user()
        # Creating new Tag instance with assigned user.
        tag = models.Tag.objects.create(user=user, name='Tag1')

        # Testing 2 things:
        # 1)Checking corect string representation setup for the model instances.
        # 2)If we can create new Tag instances.
        self.assertEqual(str(tag), tag.name)

    def test_create_ingredient(self):
        """Test creating an ingredient is successful."""
        user = create_user()
        ingredient = models.Ingredient.objects.create(
            user=user,
            name='Ingredient1',
        )

        self.assertEqual(str(ingredient), ingredient.name)
