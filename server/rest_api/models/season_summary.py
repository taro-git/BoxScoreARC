from django.db import models

from rest_api.models.game_summary import Team


class SeasonSummary(models.Model):
    season = models.CharField(primary_key=True)
    @property
    def regular_season_team_stats(self):
        return self.regular_stats.all()


class RegularSeasonTeamStats(models.Model):
    team_id = models.ForeignKey(Team, on_delete=models.PROTECT)
    season = models.ForeignKey(SeasonSummary, on_delete=models.PROTECT, related_name='regular_stats')
    conference = models.CharField()
    conference_rank = models.IntegerField()
    division = models.CharField()
    division_rank = models.IntegerField()
    win = models.IntegerField()
    lose = models.IntegerField()
    pts = models.IntegerField()
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
    def reb(self):
        return self.oreb + self.dreb
    @property
    def eff(self):
        return (self.pts + self.reb + self.ast + self.stl + self.blk) - ((self.fga - self.fg) + (self.fta - self.ft) + self.to)
    @property
    def team_abbreviation(self):
        return self.team_id.abbreviation
    @property
    def team_logo(self):
        return self.team_id.logo

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['team_id', 'season'], name='unique_team_id_season')
        ]
    



