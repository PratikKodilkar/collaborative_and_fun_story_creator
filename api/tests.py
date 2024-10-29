from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from django.contrib.auth.models import User
from .models import Story


class RegisterViewTest(APITestCase):
    def setUp(self):
        self.client = APIClient()

        self.url = reverse('register') 

        self.valid_user_data = {
            "username": "testuser",
            "password": "testpassword123",
            "confirm_password": "testpassword123",
            "email": "testuser@example.com",
            "first_name": "Test",
            "last_name": "User"
        }

        self.invalid_user_data = {
            "username": "testuser",
            "password": "testpassword123",
            "confirm_password": "wrongpassword",
            "email": "testuser@example.com",
            "first_name": "Test",
            "last_name": "User"
        }

    def test_register_valid_user(self):
        """
        Ensure we can successfully register a user with valid data.
        """
        response = self.client.post(self.url, self.valid_user_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertIn('message', response.data)
        self.assertEqual(response.data['message'], "User registered successfully")

        self.assertTrue(User.objects.filter(username="testuser").exists())

    def test_register_invalid_user(self):
        """
        Ensure registration fails with invalid data (password mismatch).
        """
        response = self.client.post(self.url, self.invalid_user_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertIn('password', response.data) 

        self.assertFalse(User.objects.filter(username="testuser").exists())
