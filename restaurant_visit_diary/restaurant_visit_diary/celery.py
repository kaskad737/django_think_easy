import os

from celery import Celery

# restaurant_visit_diary/restaurant_visit_diary

os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    'restaurant_visit_diary.settings'
    )

app = Celery(
    'restaurant_visit_diary',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0',
    )

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

if __name__ == '__main__':
    app.start()
