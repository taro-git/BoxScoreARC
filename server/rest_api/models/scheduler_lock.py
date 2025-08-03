from django.db import models


class SchedulerLock(models.Model):
    name = models.CharField(primary_key=True)
    locked_at = models.DateTimeField(auto_now=True)


class ScheduledBoxScoreStatus(models.Model):
    STATUS_CHOICES = [
        ('pending', 'pending'),
        ('progressing', 'progressing'),
    ]
    game_id = models.IntegerField(primary_key=True)
    registered_datetime = models.DateTimeField(auto_now=True)
    status = models.CharField(default='pending', choices=STATUS_CHOICES)
    progress = models.IntegerField(default=0)

