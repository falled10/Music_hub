import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'music_hub.settings')

app = Celery('music_hub', broker='redis://redis:6379')
app.config_from_object('django.conf:settings')

app.autodiscover_tasks()
