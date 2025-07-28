from django.db import models

from .game_summary import GameSummary


class BoxScore(models.Model):
    game_id = models.OneToOneField(GameSummary, on_delete=models.CASCADE, primary_key=True)
    @property
    def home_players_on_box_score(self):
        return self.players.filter(is_home=True)
    @property
    def away_players_on_box_score(self):
        return self.players.filter(is_home=False)


class BoxScorePlayer(models.Model):
    game_id = models.ForeignKey(BoxScore, on_delete=models.CASCADE, related_name='players')
    is_home = models.BooleanField()
    player_id = models.IntegerField()
    @property
    def data(self):
        return self.moment_data.all()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['game_id', 'player_id'], name='unique_box_score_game_id_player_id')
        ]


class BoxScoreData(models.Model):
    player = models.ForeignKey(BoxScorePlayer, on_delete=models.CASCADE, related_name='moment_data')
    elapsed_seconds = models.IntegerField()
    is_on_court = models.BooleanField()
    min = models.DecimalField(max_digits=5, decimal_places=2)
    pts = models.IntegerField()
    reb = models.IntegerField()
    ast = models.IntegerField()
    stl = models.IntegerField()
    blk = models.IntegerField()
    fg = models.IntegerField()
    fga = models.IntegerField()
    fgper = models.DecimalField(max_digits=5, decimal_places=2)
    three = models.IntegerField()
    threea = models.IntegerField()
    threeper = models.DecimalField(max_digits=5, decimal_places=2)
    ft = models.IntegerField()
    fta = models.IntegerField()
    ftper = models.DecimalField(max_digits=5, decimal_places=2)
    oreb = models.IntegerField()
    dreb = models.IntegerField()
    to = models.IntegerField()
    pf = models.IntegerField()
    eff = models.DecimalField(max_digits=5, decimal_places=2)
    plusminus = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['player', 'elapsed_seconds'], name='unique_box_score_player_id_elapsed_seconds')
        ]

