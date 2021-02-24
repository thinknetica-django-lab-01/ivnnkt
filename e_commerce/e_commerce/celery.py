import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'e_commerce.settings')

app = Celery('e_commerce')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'send-new-products-every-week': {
        'task': 'main.tasks.send_mailing',
        'schedule': crontab(
            minute=0,
            hour=17,
            day_of_week='fri'
        ),
    },
}


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
