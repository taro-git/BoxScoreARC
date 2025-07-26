from django.db import models


class Team(models.Model):
    team_id = models.IntegerField(primary_key=True)
    abbreviation = models.CharField()
    logo = models.CharField()


class GameSummary(models.Model):
    game_id = models.CharField(primary_key=True)
    sequence = models.IntegerField()
    status_id = models.IntegerField()
    status_text = models.CharField()
    live_period = models.IntegerField()
    live_clock = models.CharField()
    game_date_est = models.DateField()
    home_team = models.ForeignKey(Team, on_delete=models.PROTECT, related_name='home_games')
    home_score = models.IntegerField()
    away_team = models.ForeignKey(Team, on_delete=models.PROTECT, related_name='away_games')
    away_score = models.IntegerField()
    @property
    def home_players_on_game(self):
        return self.players.filter(is_home=True)
    @property
    def away_players_on_game(self):
        return self.players.filter(is_home=False)


class PlayerOnGame(models.Model):
    game_id = models.ForeignKey(GameSummary, on_delete=models.CASCADE, related_name='players')
    is_home = models.BooleanField()
    player_id = models.IntegerField()
    name = models.CharField()
    jersey = models.CharField(null=True, blank=True)
    position = models.CharField(null=True, blank=True)
    is_starter = models.BooleanField()
    is_inactive = models.BooleanField()
    sequence = models.IntegerField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['game_id', 'player_id'], name='unique_game_id_player_id')
        ]
