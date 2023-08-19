"""
Tests for Django admin modifications.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
# Django test Client that allows to make http requests
from django.test import Client


class AdminSiteRests(TestCase):
    """Tests for Django admin."""

    # Adding setup method to our test, which Will allow to \
    # setup some modules at the beginning of diferent tests \
    # that we add to this class. This setup code will be run \
    # before every other test code that we have.

    # Spelling of this name is important.
    def setUp(self):
        """Create user and client."""
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@example.com',
            password='testpass123',
        )
        # force_login() allowes to force authentication to the user.
        # Every request that we will make through this client \
        # will be authenticated with this created user.
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email='user@example.com',
            password='testpass123',
            name='Test User'
        )

    def test_users_list(self):
        """Test that users are listed on page."""
        # This URL will get the page that holds the list of users.
        # Refere to Django documentation.
        url = reverse('admin:core_user_changelist')
        # Makes HTTP Get request to this url.
        # Because we used force_login(), request will be made \
        # authenticated as the user that we forced to login.
        res = self.client.get(url)

        # We asser that page contains the name of the user\
        # that we have created. And it also contains email \
        # address.
        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_edit_user_page(self):
        """Test the edit user page works."""

        # Url for change user page
        # We need to add an ID of the user that we want to change.
        # It will get Url like this: \
        # http://127.0.0.1:8000/admin/core/user/1/change/
        url = reverse('admin:core_user_change', args=[self.user.id])
        res = self.client.get(url)

        # To be sure that page loads successfully, \
        # with http 200 responce
        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """Test the create user page works."""
        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
