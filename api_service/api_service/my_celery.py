# api_service/celery.py
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# establecer la configuración de Django predeterminada para Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api_service.settings')

app = Celery('api_service')

# usar la configuración de Django para Celery
app.config_from_object('django.conf:settings', namespace='CELERY')

# descubrir tareas de Celery en todas las aplicaciones de Django
app.autodiscover_tasks()
