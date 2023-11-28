import requests
from django.conf import settings


def get_stock_data_http(stock_code):
    return requests.get(
       f'{settings.DJANGO_STOCK_SERVICE_URL}/stock?stock_code={stock_code}'
    ).json()
