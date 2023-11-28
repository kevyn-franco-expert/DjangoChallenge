# api_service/__init__.py
from __future__ import absolute_import, unicode_literals
from .my_celery import app as celery_app

__all__ = ('celery_app',)
