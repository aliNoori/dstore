# dstore/celery.py

from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from kombu import Exchange, Queue
from pathlib import Path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dstore.settings')####'your_project_name.settings'

app = Celery('dstore')

app.config_from_object('django.conf:settings', namespace='CELERY')
broker_url = 'amqp://guest:guest@localhost:5672/'  # Your broker URL
broker_connection_retry_on_startup = True
app.conf.update(
    task_queues = (
        Queue('default', Exchange('default'), routing_key='default'),
        Queue('users', Exchange('users'), routing_key='users.#'),
        Queue('celery', Exchange('celery'), routing_key='celery'),
        Queue('send_notification', Exchange('send_notification'), routing_key='send_notification'),
        Queue('high_value_order', Exchange('high_value_order'), routing_key='high_value_order'),
        Queue('gift_to_user', Exchange('gift_to_user'), routing_key='gift_to_user'),
        Queue('charge_wallet', Exchange('charge_wallet'), routing_key='charge_wallet'),
        Queue('lottery', Exchange('lottery'), routing_key='lottery'),
        Queue('add_score', Exchange('add_score'), routing_key='add_score'),
    ),
    task_default_queue='default',
    task_default_exchange='default',
    task_default_routing_key='default',
)
BASE_DIR = Path(__file__).resolve().parent.parent
# مسیر فایل لاگ
LOG_DIR = os.path.join(BASE_DIR, 'logs/celery.log')

# تنظیمات برای ذخیره لاگ‌ها در فایل
from celery.signals import setup_logging

@setup_logging.connect
def configure_logging(sender=None, **kwargs):

    import logging
    logging.basicConfig(filename=LOG_DIR, level=logging.DEBUG)

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))