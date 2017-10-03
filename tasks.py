from __future__ import absolute_import, unicode_literals
from celery import shared_task
from celery.schedules import crontab
from great_news.celery import app
from celery.utils.log import get_task_logger

from .models import Character

logger = get_task_logger(__name__)


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(),
        test.s(),
    )

@app.task
def test():
    Character.objects.create(name="abc")
