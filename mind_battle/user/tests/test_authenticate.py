from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from user.models import User


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

        response = self.client.post("register", data=payload_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
