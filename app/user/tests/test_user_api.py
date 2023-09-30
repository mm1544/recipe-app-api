"""
Tests for the user API.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
# Will allow to get url from the name of \
# the View that we want to get that url for(?).
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

#   Setting URLs that we are going to test ###
# API url that we will be testing
# 'user' as an app and 'create' is an endpoint
# Will return a full URL path inside our project.
CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')


def create_user(**params):
    """Create and return a new user."""

    # Helper f-n that will create the user for testing.
    return get_user_model().objects.create_user(**params)


# Will be breaking into 1)Public and 2)Private tests.
# Public tests - Unauthenticated requests (don't \
# require auth. e.g. registering a new user).

class PublicUserApiTests(TestCase):
    """Test the public features of the user API."""

    def setUp(self):
        # Client used for testing
        self.client = APIClient()

    def test_create_user_success(self):
        """Test creating a user is successful."""
        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'Test Name',
        }

        # Making HTTP Post request
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password']))

        # To make sure that the password hash is not returned \
        # in the response. This is security issue. Newer need \
        # to send hash back to the user, because all the \
        # password checking is done in the database.
        self.assertNotIn('password', res.data)

    # Tests for error cases
    def test_user_with_email_exists_error(self):
        """Test error returned if user with email exists."""
        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'Test Name',
        }
        # Will cal our custom f-n
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)

        # Checking if get a bad responce back
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    # Testing case when given password is too short.
    def test_password_too_short_error(self):
        """Test an error is returned if password is less than 5 chars."""
        payload = {
            'email': 'test@example.com',
            'password': 'pw',
            'name': 'Test name',
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """Test generates token for valid credentials."""
        user_details = {
            'name': 'Test Name',
            'email': 'test@example.com',
            'password': 'test-user-password123',
        }
        create_user(**user_details)
        # 'payload' will be sent to token API to login.
        payload = {
            'email': user_details['email'],
            'password': user_details['password'],
        }
        res = self.client.post(TOKEN_URL, payload)

        # Tests if 'token' is IN res.data dictionary
        self.assertIn('token', res.data)
        # Tests if responce code is 200
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_bad_credentials(self):
        """Test returns error if credentials invalid."""
        create_user(email='test@example.com', password='goodpass')

        payload = {'email': 'test@example.com', 'password': 'badpass'}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_email_not_found(self):
        """Test error returned if user not found for given email."""
        payload = {'email': 'test@example.com', 'password': 'pass123'}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_blank_password(self):
        """Test posting a blank password returns an error."""
        payload = {'email': 'test@example.com', 'password': ''}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthorised(self):
        """Test authentication is required for users."""
        # Checking that authentication is required and enforced \
        # for ME_URL endpoint.
        res = self.client.get(ME_URL)

        # Here we make unauthenticated http request to 'me' endpoint.
        # You are not Authorised to use endpoint if you are not \
        # authenticated (!!)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


# Tests are split into 2 different classes:
# 1) Public test (unauthenticated test to the endpoint) \
# 2) Private private test (authenticated) to the endpoint.

# 2) Authenticated User testing
class PrivateUserApiTests(TestCase):
    """Test API requests that require authentication."""

    def setUp(self):
        self.user = create_user(
            email='test@example.com',
            password='testpass123',
            name='Test Name',
        )
        #  API testing client provided by REST framework
        self.client = APIClient()
        #  It forces authentication to the specific user. \
        # It is usefull because we don't have to do 'real' \
        # authentication.
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """Test retrieving profile for logged in user."""
        # Request should retrieve data from the current authenticated user.
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'name': self.user.name,
            'email': self.user.email,
        })

    def test_post_me_not_allowed(self):
        """Test POST is not allowed for the 'me' endpoint."""

        # Testing that POST method is disabled for 'me' endpoint. \
        # HTTP POST should only(!) be used when you are creating objects \
        # in the system(!). Since this endpoint(!) isn't designed to \
        # create Objects(!), that is what 'create_user' API is for, \
        # this API should disable the POST method for this endpoint.
        res = self.client.post(ME_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """Test updating the user profile for the authenticated user."""
        payload = {'name': 'Updated name', 'password': 'newpassword123'}

        res = self.client.patch(ME_URL, payload)

        # Refreshing User values on DB. By default they are not \
        # refreshed automatically. They are loaded when you first \
        # creating the user and then you need to call 'refresh_from_db' \
        # method to update that object.
        self.user.refresh_from_db()
        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
