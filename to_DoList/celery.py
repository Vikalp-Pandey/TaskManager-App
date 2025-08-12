import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'to_DoList.settings')

app = Celery('to_DoList')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()