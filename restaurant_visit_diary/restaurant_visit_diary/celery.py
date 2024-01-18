import os
import environ
from celery import Celery
env = environ.Env()
environ.Env.read_env()

REDIS_HOST = env("REDIS_HOST")

# restaurant_visit_diary/restaurant_visit_diary

os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    'restaurant_visit_diary.settings'
    )

app = Celery(
    'restaurant_visit_diary',
    broker=f'redis://{REDIS_HOST}:6379/0',
    backend=f'redis://{REDIS_HOST}:6379/0',
    )

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

if __name__ == '__main__':
    app.start()
