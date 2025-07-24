from django.core.exceptions import ValidationError
from django.db import models


class TeamOnGame(models.Model):
    game_id = models.CharField()
    team_id = models.IntegerField()
    abbreviation = models.CharField()
    logo = models.CharField()
    score = models.IntegerField()
    is_home = models.BooleanField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['game_id', 'is_home'], name='unique_game_id_is_home'),
            models.UniqueConstraint(fields=['game_id', 'team_id'], name='unique_game_id_team_id'),
        ]

class GameSummary(models.Model):
    game_id = models.CharField(primary_key=True)
    sequence = models.IntegerField()
    status_id = models.IntegerField()
    status_text = models.CharField()
    live_period = models.IntegerField()
    live_clock = models.CharField()
    game_date_est = models.DateField()
    home_team = models.OneToOneField(TeamOnGame, on_delete=models.CASCADE, related_name='home_team_on_game')
    away_team = models.OneToOneField(TeamOnGame, on_delete=models.CASCADE, related_name='away_team_on_game')

    def _clean(self):
        errors = {}

        if self.home_team.game_id != self.game_id:
            errors['home_team'] = "Home team must belong to this game."
        if self.away_team.game_id != self.game_id:
            errors['away_team'] = "Away team must belong to this game."

        if self.home_team.team_id == self.away_team.team_id:
            errors['team_id'] = "Home and away teams must be different."

        if not self.home_team.is_home:
            errors['home_team_is_home'] = "Home team must have is_home=True."
        if self.away_team.is_home:
            errors['away_team_is_home'] = "Away team must have is_home=False."

        if errors:
            raise ValidationError(errors)
        
    def save(self, *args, **kwargs):
        self._clean()
        super().save(*args, **kwargs)
    
    def upsert(self):
        self._clean()
        self.__class__.objects.update_or_create(
            game_id=self.game_id,
            defaults={
                'sequence': self.sequence,
                'status_id': self.status_id,
                'status_text': self.status_text,
                'live_period': self.live_period,
                'live_clock': self.live_clock,
                'game_date_est': self.game_date_est,
                'home_team': self.home_team,
                'away_team': self.away_team,
            }
        )


class PlayerOnGame(models.Model):
    team_on_game = models.ForeignKey(TeamOnGame, on_delete=models.CASCADE)
    player_id = models.IntegerField()
    name = models.CharField()
    jersey = models.CharField(null=True, blank=True)
    position = models.CharField(null=True, blank=True)
    is_starter = models.BooleanField()
    is_inactive = models.BooleanField()
    sequence = models.IntegerField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['team_on_game', 'player_id'], name='unique_team_on_game_player_id')
        ]
