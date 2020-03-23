from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken
from rest_framework_simplejwt.tokens import RefreshToken
from django.urls import reverse
from django.contrib.auth import get_user_model


class TestRegisterUser(APITestCase):
    """Test suite for registering new user."""

    def test_create_new_account(self):

        payload_data = {
            "username": "user1",
            "password": "secret",
            "re_password": "secret",
            "email": "email@gmail.com",
            "age": 20
        }

        response = self.client.post(reverse("register"), data=payload_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class TestAuthUserJWTTokenAuthentication(APITestCase):
    """Test suite for logging user using JWT Token authentication backend."""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='user',
            password='password',
            email='email@gmail.com'
        )
        self.user_payload_data = {
            'username': 'user',
            'password': 'password'
        }

    def test_login_token_retrieve_successful(self):
        """Assert tokens are obtained on successful credentials passed."""

        response = self.client.post(reverse('login'), data=self.user_payload_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data.get('access'))
        self.assertIsNotNone(response.data.get('refresh'))

    def test_logout_user_success(self):
        """Assert logout endpoint expire immediatelly user token."""
        self.client.force_authenticate(self.user)
        res = self.client.post(reverse('login'), data=self.user_payload_data)
        token = res.data['refresh']

        response = self.client.post(reverse('logout'), data={'refresh': token})

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(BlacklistedToken.objects.count(), 1)

    def test_only_logged_in_user_can_logout(self):
        """Make sure only logged in user can access logout endpoint."""
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
