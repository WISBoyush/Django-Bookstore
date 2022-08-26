
from __future__ import absolute_import
import os
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bookstore.settings')

# здесь вы меняете имя
app = Celery("bookstore", backend='redis://localhost')

app.conf.broker_url = 'redis://localhost:6379/0'

app.conf.result_backend = 'redis://localhost:6379/0'

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


# @app.task(bind=True)
# def debug_task(self):
#     print(f'Request: {self.request!r}')
