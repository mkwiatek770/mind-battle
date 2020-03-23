from rest_framework.test import APITestCase
from rest_framework import status
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


class TestLoginUser(APITestCase):
    """Test suite for logging user using TokenAuthentication backend."""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='user',
            password='password',
            email='email@gmail.com'
        )

    def test_login_token_retrieve_successful(self):
        """Assert token is obtained on successful credentials passed."""
        payload_data = {'username': 'user', 'password': 'password'}

        response = self.client.post(reverse('login'), data=payload_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data['token'])
