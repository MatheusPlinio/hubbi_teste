from celery.schedules import crontab
import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

app = Celery("core")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.beat_schedule = {
    "replenish-stock-every-day": {
        "task": "inventory.tasks.daily_stock_replenish",
        "schedule": crontab(hour=0, minute=0),
    },
}
