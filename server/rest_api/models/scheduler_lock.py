from django.db import models


class SchedulerLock(models.Model):
    name = models.CharField(primary_key=True)
    locked_at = models.DateTimeField(auto_now=True)
