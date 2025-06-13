from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()

class RegistrationTest(APITestCase):
    def test_registration(self):
        url = reverse('registration')
        data = {
            'fullname': 'Test User',
            'email': 'test@example.com',
            'password': 'testpass123',
            'repeated_password': 'testpass123'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('token', response.data)
        self.assertEqual(response.data['email'], 'test@example.com')
