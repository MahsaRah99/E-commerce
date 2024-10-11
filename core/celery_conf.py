import os

from celery import Celery
from celery.schedules import crontab
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

celery_app = Celery("core")
celery_app.config_from_object("django.conf:settings", namespace="CELERY")
celery_app.autodiscover_tasks(related_name="tasks")

celery_app.conf.broker_url = settings.CACHES["default"]["LOCATION"]
celery_app.conf.result_backend = settings.CACHES["default"]["LOCATION"]
celery_app.conf.broker_connection_retry_on_startup = True

celery_app.conf.beat_schedule = {
    "deactive_expired_carts_every_minute": {
        "task": "store.tasks.deactive_expired_carts",
        "schedule": crontab(),
    }
}
