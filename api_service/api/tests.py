import os
import sys

import django
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api_service.settings')

django.setup()


class StockViewTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='user', password='password')
        self.client.login(username='user', password='password')

    def test_stock_view_without_stock_code(self):
        url = reverse('stock')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class HistoryViewTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='user', password='password')
        self.client.login(username='user', password='password')

    def test_history_view(self):
        url = reverse('history')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class StatsViewTests(APITestCase):

    def setUp(self):
        self.superuser = User.objects.create_superuser(username='superuser', password='password')
        self.user = User.objects.create_user(username='user', password='password')
        self.client.login(username='superuser', password='password')

    def test_stats_view_as_superuser(self):
        url = reverse('stats')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_stats_view_as_non_superuser(self):
        self.client.login(username='user', password='password')
        url = reverse('stats')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
