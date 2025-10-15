import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
 
app = Celery('myproject')
app.config_from_object('django.conf:settings', namespace = 'CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'send_email_every_monday': {
        'task': 'news.tasks.send_email_every_monday',
        'schedule': crontab(minute = 0, hour = 8, day_of_week = 'monday'),
    },
}