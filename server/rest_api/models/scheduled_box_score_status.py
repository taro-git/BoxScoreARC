from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from rest_api.models.game_summary import GameSummary


class ScheduledBoxScoreStatus(models.Model):
    game_id = models.OneToOneField(GameSummary, primary_key=True, on_delete=models.CASCADE)
    registered_datetime = models.DateTimeField(auto_now=True)
    error_message = models.CharField(null=True, blank=True)
    progress = models.IntegerField(
        default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100),
        ],
    )

    @property
    def status(self):
        return (
            "errored"
            if self.error_message
            else "pending"
            if self.progress == 0
            else "completed"
            if self.progress == 100
            else "progressing"
        )
