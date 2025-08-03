from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from django.db import models

from rest_api.models.scheduler_lock import SchedulerLock


def initialize(lock_name: str):
    SchedulerLock.objects.filter(~models.Q(name=lock_name)).delete()

