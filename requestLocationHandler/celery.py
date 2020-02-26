import os

from celery import Celery
from django.conf import settings

# Set Celery settings:
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'requestLocationHandler.settings')

# Initiate Celery app:
app = Celery('requestLocationHandler')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
