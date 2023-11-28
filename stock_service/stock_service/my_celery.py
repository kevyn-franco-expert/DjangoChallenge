# api_service/celery.py
from __future__ import absolute_import, unicode_literals

import os

from celery import Celery
from django.conf import settings

# from stocks.tasks import get_stock_data

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stock_service.settings')

app = Celery('stock_service')

app.config_from_object('django.conf:settings', namespace='CELERY_')

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# app.register_task(get_stock_data)
