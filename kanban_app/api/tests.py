from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from kanban_app.models import Board

User = get_user_model()

class BoardAPITestCase(APITestCase):
    """Test basic Board API functionality."""
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='testpass', fullname='Test User')
        self.client.force_authenticate(user=self.user)

    def test_create_board(self):
        url = reverse('board-list')
        data = {'title': 'Test Board', 'members': [self.user.id]}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Board.objects.count(), 1)
        self.assertEqual(Board.objects.get().title, 'Test Board')

    def test_list_boards(self):
        Board.objects.create(title='Board 1', owner=self.user)
        url = reverse('board-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) >= 1)
