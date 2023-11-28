import os
import sys

import django
import requests_mock
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stock_service.settings')

django.setup()


class StockViewTests(TestCase):

    def setUp(self):
        self.url = reverse('stock-view')

    @requests_mock.Mocker()
    def test_get_stock_success(self, mock):
        mock.get('https://stooq.com/q/l/?s=aapl.us&f=sd2t2ohlcvn&h&e=csv',
                 text='Symbol,Date,Time,Open,High,Low,Close,Volume,Name\nAAPL.US,2023-11-27,22:00:13,189.92,190.67,188.9,189.79,30984740,APPLE\n')

        response = self.client.get(self.url, {'stock_code': 'aapl.us'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('AAPL.US', response.content.decode())

    def test_get_stock_no_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @requests_mock.Mocker()
    def test_get_stock_api_fail(self, mock):
        mock.get('https://stooq.com/q/l/?s=aapl.us&f=sd2t2ohlcvn&h&e=csv', status_code=500)

        response = self.client.get(self.url, {'stock_code': 'aapl.us'})
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
