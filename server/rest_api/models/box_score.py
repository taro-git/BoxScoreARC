from django.db import models

from rest_api.models.scheduled_box_score_status import ScheduledBoxScoreStatus


class BoxScore(models.Model):
    game_id = models.OneToOneField(ScheduledBoxScoreStatus, primary_key=True, on_delete=models.CASCADE)
    final_seconds = models.IntegerField()
    @property
    def final_period(self):
        return 4 + round((self.final_seconds - 4 * 12 * 60)/(5*60))
    @property
    def is_collect(self):
        home_players = self.home_players_on_box_score
        home_sec = 0
        home_pts = 0
        home_plusminus = 0
        for home_player in home_players:
            final_data = home_player.moment_data.last()
            if final_data:
                home_sec += final_data.sec
                home_pts += final_data.pts
                home_plusminus += final_data.plusminus

        away_players = self.away_players_on_box_score
        away_sec = 0
        away_pts = 0
        away_plusminus = 0
        for away_player in away_players:
            final_data = away_player.moment_data.last()
            if final_data:
                away_sec += final_data.sec
                away_pts += final_data.pts
                away_plusminus += final_data.plusminus
        return (home_pts - away_pts)*5 == home_plusminus and home_plusminus + away_plusminus == 0 and self.final_seconds*5 == home_sec and home_sec == away_sec
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
    sec = models.IntegerField()
    @property
    def min(self):
        return round(self.sec/60, 1)
    pts = models.IntegerField()
    reb = models.IntegerField()
    ast = models.IntegerField()
    stl = models.IntegerField()
    blk = models.IntegerField()
    fg = models.IntegerField()
    fga = models.IntegerField()
    three = models.IntegerField()
    threea = models.IntegerField()
    ft = models.IntegerField()
    fta = models.IntegerField()
    oreb = models.IntegerField()
    dreb = models.IntegerField()
    to = models.IntegerField()
    pf = models.IntegerField()
    plusminus = models.IntegerField()
    @property
    def eff(self):
        return (self.pts + self.reb + self.ast + self.stl + self.blk) - ((self.fga - self.fg) + (self.fta - self.ft) + self.to)

